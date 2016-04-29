"""
Main service functions of practice app.
"""

import logging

from collections import namedtuple
from common.flow_factors import FlowFactors
from tasks.models import TaskModel
from tasks.services.task_service import get_toolbox_from_blocks
from practice.models.practice_context import create_practice_context
from practice.models import TaskInstanceModel
from practice.models import StudentTaskInfoModel
from practice.models import StudentModel
from practice.models.task_instance import FlowRating
from practice.services.parameters_update import update_parameters
from practice.services import practice_session_service as sess_service
from practice.services import statistics_service
from practice.services.details import get_practice_details
from practice.services.levels import try_levelup
from practice.core.credits import compute_credits
from practice.core.task_filtering import filter_tasks_by_level
from practice.core.task_selection import RandomTaskSelector, IdSpecifidedTaskSelector
from concepts.models import Instruction
import json

logger = logging.getLogger(__name__)

# TODO: remove task field - it is redundant (task is in task_instance.task)
TaskInfo = namedtuple('TaskInfo',
        ['task_instance', 'task', 'toolbox', 'instructions', 'session'])
SessionOverview = namedtuple('SessionOverview',
        ['task_instances', 'overall_time', 'percentils'])

def get_task_by_id(user, task_id):
    student = StudentModel.objects.get_or_create(user=user)[0]
    # ask if the student is in the middle of the session task
    if sess_service.has_unresolved_task(student):
        session = sess_service.get_session(student)
        active_task = sess_service.get_active_task_instance(session)
        if active_task.task.pk == task_id:
            # if the given task is same as active, go in session
            return get_active_task_in_session(student)
    return get_task(student, IdSpecifidedTaskSelector(task_id))


def get_next_task_in_session(user):
    student = StudentModel.objects.get_or_create(user=user)[0]
    if sess_service.has_unresolved_task(student):
        return get_active_task_in_session(student)
    # next task in the session or new session
    task_info = get_task(student, RandomTaskSelector())
    sess_service.next_task_in_session(student, task_info.task_instance)
    # add info about session
    session = sess_service.get_session(student)
    task_info_with_sess = TaskInfo(
        task_instance = task_info.task_instance,
        task = task_info.task,
        toolbox = task_info.toolbox,
        instructions = task_info.instructions,
        session = session
    )
    return task_info_with_sess


def get_active_task_in_session(student):
    session = sess_service.get_session(student)
    active_task_instance = sess_service.get_active_task_instance(session)
    if not active_task_instance:
        raise ValueError('Student {pk} does not have an active task.')
    session_task_instance_info = TaskInfo(
        task_instance = active_task_instance,
        task = active_task_instance.task,
        toolbox = get_student_toolbox(student),
        instructions = get_instructions(student, active_task_instance.task),
        session = session
    )
    return session_task_instance_info


def get_task(student, task_selector):
    """
    Return next task for given student. Also create a new task instance record
    in DB and update student-task info for selected task (namely the reference
    to last task instance).

    Returns:
        TaskInfo namedtuple

    Raises:
        ValueError: If the student argument is None.
        LookupError: If there is no task available.
    """
    if not student:
        raise ValueError('Student is required for get_task')
    logger.info("Getting next task for student id %s", student.pk)
    practice_context = create_practice_context(student=student)
    #task_ids = practice_context.get_all_task_ids()
    tasks = filter_tasks_by_level(TaskModel.objects.all(), student)
    if not tasks:
        raise LookupError('No tasks available.')
    task_ids = [task.pk for task in tasks]
    task_id = task_selector.select(task_ids, student.pk, practice_context)
    #predicted_flow = predict_flow(student.pk, task_id, practice_context)
    task = TaskModel.objects.get(pk=task_id)
    task_instance = TaskInstanceModel.objects.create(student=student, task=task)
    student_task_info = StudentTaskInfoModel.objects.get_or_create(
            student=student, task=task)[0]
    student_task_info.last_instance = task_instance
    student_task_info.save()
    instructions = get_instructions(student, task)

    task_info = TaskInfo(
        task_instance = task_instance,
        task = task,
        toolbox = get_student_toolbox(student),
        instructions = instructions,
        session = None
    )
    logger.info("Task %s successfully picked for student %s", task_id, student.pk)
    return task_info

def get_student_toolbox(student):
    """Fetches the user toolbox.

    Args:
        student: current stuent practicing tasks

    Returns:
        list of identifiers of all available blocks for the user
    """
    details = get_practice_details(student.user)
    return get_toolbox_from_blocks(details.available_blocks)


def process_attempt_report(user, report):
    """Process reported result of a solution attempt of a task

    Args:
        user: current user (user who took the attempt
        report: dictionary with the following fiels:
            - task-instance-id
            - attempt
            - solved
            - time
    Returns:
        - whether the task is solved for the first time
        - number of earned-credits
        - speed-bonus: bool
    Raises:
        ValueError:
            - If the user argument is None.
            - If the report doesn't belong to the student.
            - If it's reporting an obsolete attempt (i.e. new attempt was
              already processed).
    """
    student = StudentModel.objects.get(user=user)
    # TODO: move the parsing of parameters to the view
    task_instance_id = report['task-instance-id']
    attempt_count = report['attempt']
    solved = report['solved']
    time = report['time']

    logger.info("Reporting attempt for student %s with result %s", student.pk, solved)
    task_instance = TaskInstanceModel.objects.get(id=task_instance_id)
    if  attempt_count < task_instance.attempt_count:
        # It means that this report is obsolete. Note that we allow for
        # equality of attempts count, which means that we want to update the
        # last report with more information (e.g. added flow report).
        raise ValueError("Obsolete attempt report can't be processed.")

    if student.pk != task_instance.student.pk:
        raise ValueError("Report doesn't belong to the student.")

    task_instance.update_after_attempt(
            attempt_count=attempt_count,
            time=time,
            solved=solved,
    )
    task_instance.save()
    task = task_instance.task
    student_task_info = StudentTaskInfoModel.objects.get_or_create(student=student, task=task)[0]
    solved_before = student_task_info.last_solved_instance is not None
    student_task_info.update(task_instance)
    student_task_info.save()

    if solved:
        see_task_concepts(student, task)

    credits = 0
    speed_bonus = False
    purchases = []
    if solved:
        task = task_instance.task
        if not solved_before:
            percentil = statistics_service.percentil(task_instance)
            level = task.toolbox.level
            credits, speed_bonus = compute_credits(level, percentil)
            student.earn_credits(credits)
            task_instance.earned_credits = credits
            task_instance.speed_bonus = speed_bonus

            levelup_achieved = try_levelup(student)
            if levelup_achieved:
                purchases.extend(student.toolbox.get_new_blocks())
                #logger.debug('Student {0} bought block {1}'.format(student.pk, new_block))

            student.save()
            task_instance.save()

    task_solved_first_time = solved and not solved_before,
    logger.info("Reporting attempt was successful for student %s with result %s", student.pk, solved)
    result = namedtuple('processAttemptReportResult',
                        ['task_solved_first_time', 'credits', 'speed_bonus', 'purchases'])\
                        (task_solved_first_time, credits, speed_bonus, purchases)
    return result


def see_task_concepts(student, task):
    for concept in task.get_contained_concepts():
        student.mark_concept_as_seen(concept)

def process_giveup_report(user, task_instance_id, time_spent):
    student = StudentModel.objects.get(user=user)
    task_instance = TaskInstanceModel.objects.get(id=task_instance_id)
    if student.pk != task_instance.student.pk:
        raise ValueError("Report doesn't belong to the student.")
    task_instance.update_after_giveup(time_spent=time_spent)
    task_instance.save()
    reported_flow = FlowRating.VERY_DIFFICULT
    process_flow_report(user, task_instance_id, reported_flow)


def process_flow_report(user, task_instance_id, reported_flow=None):
    """Process reported flow after the task completion (or giving up)
    """
    if not reported_flow:
        return
    student = StudentModel.objects.get(user=user)
    task_instance = TaskInstanceModel.objects.get(id=task_instance_id)
    if student.pk != task_instance.student.pk:
        raise ValueError("The task instance doesn't belong to this student.")
    task_instance.set_reported_flow(reported_flow)
    task_instance.save()

    ## NOTE: temporarily, we are using a dummy models without parameters, so
    ## there is nothing to update
    #task = task_instance.task
    #practice_context = create_practice_context(student=student, task=task)
    #update_parameters(practice_context, student.pk, task.pk,
    #        task_instance.get_reported_flow(),
    #        task_instance.get_predicted_flow(),
    #        _get_last_solved_delta(student, task))
    ## NOTE: There is a race condition when 2 students are updating parameters
    ## for the same task at the same time. In the current conditons, this is
    ## rare and if it happens it does not cause any problems (one update is
    ## ignored). But if it changes in the future (many users using the system at
    ## the same time), then we might want to eliminate the race condition.
    ## Possible solution is probably to use select_for_update, but then it's
    ## necessary to make sure that there is as little blocking as possible
    ## (assigning update functions to the practice_context then
    ## select_for_update current parameters, update them at once ("in parallel")
    ## and save.
    #practice_context.save()

def get_session_overview(user):
    """
    Returns information about the last session student has been practicing.

    Returns:
        namedtuple 'session_overview'
    """
    student = StudentModel.objects.get_or_create(user=user)[0]
    session = sess_service.get_session(student)
    if session is None:
        instances = []
    else:
        instances = session.get_task_instances()
        if instances == [] or instances[-1].time_end is None:
            overall_time = 0
        else:
            overall_delta = instances[-1].time_end - instances[0].time_start
            overall_time = overall_delta.seconds
    percentils = []
    for instance in instances:
        percentils.append(statistics_service.percentil(instance) if instance.solved else None)
    return SessionOverview(
            task_instances = instances,
            overall_time = overall_time,
            percentils = percentils
            )

def _get_last_solved_delta(student, task):
    """
    Returns time delta in seconds between solving of the last two instances
    of the task by the student. None if there is only one or none instance.

    Returns:
        integer - seconds as time delta
    """
    task_instances = TaskInstanceModel.objects.filter(
            student=student, task=task).order_by('-time_end')
    if len(task_instances) > 1 \
       and task_instances[0].time_end is not None \
       and task_instances[1].time_end is not None:
        delta = task_instances[0].time_end - task_instances[1].time_end
        return int(delta.total_seconds())
    else:
        return None

def get_instructions(student, task):
    if student is None or task is None:
        return []
    seen_concepts = student.get_seen_concepts()
    task_concepts   = task.get_contained_concepts()
    concepts = task_concepts.difference(seen_concepts)
    instructions = []
    for concept in concepts:
        instructions = instructions + list(Instruction.objects.filter(concept=concept))
    return instructions

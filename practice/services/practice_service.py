"""
Main service functions of practice app.
"""

import logging
from tasks.models import TaskModel
from practice.models.practice_context import create_practice_context
from practice.models import TaskInstanceModel
from practice.models import StudentTaskInfoModel
#from practice.services.task_selection import RandomTaskSelector as TaskSelector
from practice.services.task_selection import ScoreTaskSelector as TaskSelector
from practice.services.flow_prediction import predict_flow
from practice.services.parameters_update import update_parameters
from practice.services.instructions_service import get_instructions

logger = logging.getLogger(__name__)

def get_next_task(student):
    """
    Return next task for given student. Also create a new task instance record
    in DB and update student-task info for selected task (namely the reference
    to last task instance).

    Returns:
        dictionary with information about assigned task

    Raises:
        ValueError: If the student argument is None.
        LookupError: If there is no task available.
    """
    logger.info("Getting next task for student id %s", student.id)
    if not student:
        raise ValueError('Student is required for get_next_task')

    practice_context = create_practice_context(student=student)
    task_ids = practice_context.get_all_task_ids()
    if not task_ids:
        raise LookupError('No tasks available.')

    task_selector = TaskSelector()
    task_id = task_selector.select(task_ids, student.id, practice_context)
    predicted_flow = predict_flow(student.id, task_id, practice_context)
    task = TaskModel.objects.get(pk=task_id)
    task_instance = TaskInstanceModel.objects.create(student=student,
            task=task, predicted_flow=predicted_flow)
    student_task_info = StudentTaskInfoModel.objects.get_or_create(
            student=student, task=task)[0]
    student_task_info.last_instance = task_instance
    student_task_info.save()

    instructions = get_instructions(student, task)

    task_dictionary = task.to_json()
    task_instance_dictionary = {
        'task-instance-id': task_instance.pk,
        'task': task_dictionary,
        'instructions': instructions
    }
    logger.info("Task %s successfully picked for student %s", task_id, student.id)
    return task_instance_dictionary


def process_attempt_report(student, report):
    """Process reported result of a solution attempt of a task

    Args:
        student: user who took the attempt
        report: dictionary with the fields specified in:
            https://github.com/effa/flocs/wiki/Server-API#apipracticeattempt-report
    Raises:
        ValueError:
            - If the student argument is None.
            - If the report doesn't belong to the student.
            - If it's reporting an obsolete attempt (i.e. new attempt was
              already processed).
    """
    if not student:
        raise ValueError('Student is required for process_task_result')

    task_instance_id = report['task-instance-id']
    attempt_count = report['attempt']
    solved = report['solved']
    time = report['time']
    reported_flow = report.get('flow-report')

    logger.info("Reporting attempt for student %s with result %s", student.id, solved)

    task_instance = TaskInstanceModel.objects.get(id=task_instance_id)
    if  attempt_count < task_instance.attempt_count:
        # It means that this report is obsolete. Note that we allow for
        # equality of attempts count, which means that we want to update the
        # last report with more information (e.g. added flow report).
        raise ValueError("Obsolete attempt report can't be processed.")

    if student.id != task_instance.student.id:
        raise ValueError("Report doesn't belong to the student.")

    task_instance.update_after_attempt(
            attempt_count=attempt_count,
            time=time,
            solved=solved,
            reported_flow=reported_flow
    )
    task_instance.save()

    # Currently, we only update parameters, when the "task completion" report
    # is sent (which means that the task was solved and flow was reported)
    # TODO: there should be more explicit control (condition) for not updating
    # parameters twice (e.g. the following would not work correctly, if the
    # report comes duplicated).
    if not solved or not reported_flow:
        return

    task = task_instance.task
    practice_context = create_practice_context(student=student, task=task)
    practice_context.update('solution-count', task=task.id, update=lambda n: n + 1)
    update_parameters(practice_context, student.id, task.id,
            task_instance.get_reported_flow(),
            task_instance.get_predicted_flow())

    # NOTE: There is a race condition when 2 students are updating parameters
    # for the same task at the same time. In the current conditons, this is
    # rare and if it happens it does not cause any problems (one update is
    # ignored). But if it changes in the future (many users using the system at
    # the same time), then we might want to eliminate the race condition.
    # Possible solution is probably to use select_for_update, but then it's
    # necessary to make sure that there is as little blocking as possible
    # (assigning update functions to the practice_context then
    # select_for_update current parameters, update them at once ("in parallel")
    # and save.
    practice_context.save()
    logger.info("Reporting attempt was successful for student %s with result %s", student.id, solved)


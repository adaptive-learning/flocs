"""
Main service functions of practice app.
"""

from tasks.models import TaskModel
from practice.models.practice_context import create_practice_context
from practice.models import TaskInstanceModel
#from practice.services.task_selection import RandomTaskSelector as TaskSelector
from practice.services.task_selection import ScoreTaskSelector as TaskSelector
from practice.services.flow_prediction import predict_flow

def get_next_task(student):
    """Return next task for given student.

    Returns:
        dictionary with settings for next task

    Raises:
        ValueError: If the student argument is None.
        LookupError: If there is no task available.
    """
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

    task_dictionary = task.to_json()
    task_dictionary['task-instance-id'] = task_instance.pk
    return task_dictionary


def process_attempt_report(student, report):
    """Process reported result of a solution attempt of a task

    Args:
        student: user who took the attempt
        report: dictionary with the fields specified in:
            https://github.com/effa/flocs/wiki/Server-API#apipracticeattempt-report
    Raises:
        ValueError: If the student argument is None.
    """
    if not student:
        raise ValueError('Student is required for process_task_result')

    task_instance_id = report['task-instance-id']
    attempt_count = report['attempt']
    solved = report['result']['solved']
    time = report['result']['time']
    reported_flow = report.get('flow-report')

    task_instance = TaskInstanceModel.objects.get(id=task_instance_id)
    if  attempt_count <= task_instance.attempt_count:
        # it means that this report is obsolete
        return

    if student.id != task_instance.student.id:
        raise ValueError("Report doesn't belong to the student.")

    task_instance.update_after_attempt(attempt_count=attempt_count, time=time,
            solved=solved, reported_flow=reported_flow)
    task_instance.save()

    if not solved:
        return

    task = task_instance.task
    practice_context = create_practice_context(student=student, task=task)
    practice_context.update('solution-count', task=task.id, update=lambda n: n + 1)
    # TODO: normalizace reported_flow
    # TODO: call update of model parameters
    # with the args: task_id, student_id, reported_flow, predicted_flow, practice_context
    #print('call update of model parameters ...', student.id, task.id,
    #        task_instance.get_reported_flow(), task_instance.get_predicted_flow())
    practice_context.save()

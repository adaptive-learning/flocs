"""
Main service functions of practice app.
"""

from tasks.models import TaskModel

from practice.models.practice_context import create_practice_context
#from practice.services.task_selection import RandomTaskSelector as TaskSelector
from practice.services.task_selection import ScoreTaskSelector as TaskSelector

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

    task = TaskModel.objects.get(pk=task_id)
    task_dictionary = task.to_json()
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

    if not report['solved']:
        return

    task = TaskModel.objects.get(id=report['task-id'])
    reported_flow = report['flow-report']
    practice_context = create_practice_context(student=student, task=task)
    # TODO: call update of model parameters
    # with the args: task_id, student_id, reported_flow, predicted_flow, practice_context
    practice_context.save()





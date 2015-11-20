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

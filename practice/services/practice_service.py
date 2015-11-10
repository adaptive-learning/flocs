"""
Main service functions of practice app.
"""

from tasks.models import TaskModel
from practice.services.task_selection import ScoreTaskSelector as TaskSelector

def get_next_task():
    """Return next task (TODO: for current user)

    Returns:
        dictionary with settings for next task

    Raises:
        LookupError: If there is no task available.
    """
    tasks = TaskModel.objects.all()
    if not tasks:
        raise LookupError('No tasks available.')
    task_selector = TaskSelector()
    task = task_selector.select(tasks, student=None, practice_context=None)
    task_dictionary = task.to_json()
    return task_dictionary

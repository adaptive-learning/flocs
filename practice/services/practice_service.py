"""
Main service functions of practice app.
"""

from tasks.models import TaskModel

from practice.services.task_selection import RandomTaskSelector as TaskSelector
#from practice.services.task_selection import ScoreTaskSelector as TaskSelector

def get_next_task(student):
    """Return next task for given student.

    Returns:
        dictionary with settings for next task

    Raises:
        LookupError: If there is no task available.
    """
    tasks = TaskModel.objects.all()
    if not tasks:
        raise LookupError('No tasks available.')
    task_selector = TaskSelector()

    # TODO: use ScoreTaskSelector: pass correct parameters!
    task = task_selector.select(tasks, student=student, practice_context=None)

    task_dictionary = task.to_json()
    return task_dictionary

"""Service layer (domain model) of practice app
"""
from practice.models import TaskModel

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
    # NOTE: for now, we just take a first item
    task = tasks.first()
    task_dictionary = task.to_json()
    return task_dictionary

"""Service layer (domain model) of practice app
"""
from tasks.models import TaskModel

def get_all_tasks():
    """Return all tasks in the db.

    Returns:
        dictionary with all tasks
    """

    tasks = TaskModel.objects.all()
    # if there is no task, return empty dict
    if not tasks:
        return {}
    # get ids of all the tasks
    id_list = []
    for task in tasks:
        id_list.append(task.pk)
    return id_list

def get_task_by_id(request_id):
    """Return task by its id.

    Returns:
        dictionary with the task settings

    Raises:
        LookupError when there is no task with such an id

    """
    try:
        task = TaskModel.objects.get(id = request_id)
    except TaskModel.DoesNotExist:
        raise LookupError('Task with id ' + str(request_id) + ' does not exist.')
    return task.to_json()

# TODO: remove this redundant call (it became a complete duplicate of
# get_task_by_id
def get_task_by_id_with_toolbox(request_id):
    """Return task by its id. Include minimal required toolbox.

    Returns:
        dictionary with the task settings

    Raises:
        LookupError when there is no task with such an id

    """
    try:
        task = TaskModel.objects.get(id = request_id)
    except TaskModel.DoesNotExist:
        raise LookupError('Task with id ' + str(request_id) + ' does not exist.')
    response = task.to_json()
    return response

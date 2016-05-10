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
    response['workspace-settings']['toolbox'] = get_toolbox_from_blocks(
            task.toolbox.get_all_blocks())
    return response

def get_toolbox_from_blocks(blocks):
    """Returns usable toolbox generated from the list of blocks.

    Args:
        blocks: list of blocks that will compose the toolbox

    Returns:
        list of strings (idenfitifiers)
    """
    toolbox = []
    toolbox_condensed = []
    for block in blocks:
        toolbox += block.get_identifiers_list()
        toolbox_condensed += block.get_identifiers_condensed_list()
    # 10 is a magic constant defining maxium number of blocs before changing to
    # condensed versions. It does correspond to roughly the limit of screen
    # with height of 766 px.
    if len(toolbox) > 10:
        return toolbox_condensed
    else:
        return toolbox

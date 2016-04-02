from django.shortcuts import render

"""Access layer (controller) of tasks app
"""

from django.http import JsonResponse
from django.http import Http404
from tasks.services import task_service

def get_all_tasks(request):
    """Return an object with IDs of all task.

    Example: {"ids": [1, 2, 3]}
    """
    id_list = task_service.get_all_tasks()
    return JsonResponse({'ids' : id_list})


def get_task_by_id(request, id):
    """Get task by its id.

    Example of returned task:
    {
        "task-id": 1,
        "title": "Three steps forward",
        "maze-settings": {
            "grid": [ ... ]
            "hero": {
                "position": [1, 4],
                "direction": 0
            }
        },
    }
    """
    try:
        task = task_service.get_task_by_id(id)
    except LookupError as ex:
        raise Http404(ex)

    return JsonResponse(task)

def get_task_by_id_with_toolbox(request, id):
    """Get task by its id.

    Example of returned task:
    {
        "task-id": 1,
        "title": "Three steps forward",
        "maze-settings": {
            "grid": [ ... ]
            "hero": {
                "position": [1, 4],
                "direction": 0
            }
        }
        "workspace-settings": {
            "toolbox":  ["maze_move_forward", "maze_turn"],
            "blocksLimit": 7
        }
    }
    """
    try:
        return JsonResponse(task_service.get_task_by_id_with_toolbox(id))
    except LookupError as ex:
        raise Http404(ex)

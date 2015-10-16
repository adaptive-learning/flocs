from django.shortcuts import render

"""Access layer (controller) of tasks app
"""

from django.http import JsonResponse
from django.http import Http404
from tasks.services import task_service


def get_all_tasks(request):
    """Return response with all task.
    """
    id_list = task_service.get_all_tasks()
    return JsonResponse({'ids' : id_list})


def get_task_by_id(request, id):
    """Get task by its id.
    """
    try:
        task = task_service.get_task_by_id(id)
    except LookupError as ex:
        raise Http404(ex)

    return JsonResponse(task)

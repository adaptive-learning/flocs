"""Access layer (controller) of practice app
"""

from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from practice.services import task_service


def get_next_task(request):
    """Return response with next task.
    """
    task = task_service.get_next_task()
    return JsonResponse(task)


def post_task_result(request):
    """Store and process task result.
    """
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')

    #data = json.loads(request.body)
    #user=request.user
    # TODO: store and process the result

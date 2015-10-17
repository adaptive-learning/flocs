"""Access layer (controller) of practice app
"""

from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from practice.services import practice_service


def get_next_task(request):
    """Return response with next task.
    """
    task = practice_service.get_next_task()
    return JsonResponse(task)


def post_task_result(request):
    """Store and process task result.
    """
    print('jopA')
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')

    print('jop')
    #data = json.loads(request.body)
    #print('post_task_result:', data)
    #user=request.user
    # TODO: store and process the result

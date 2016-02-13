"""Access layer (controller) of practice app
"""

from lazysignup.decorators import allow_lazy_user
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from django.http import Http404
import json

from common.logUtils import LoggingUtils
from practice.services import practice_service

logger = LoggingUtils()


@allow_lazy_user
def get_next_task(request):
    """Return response with next task.
    """
    logger.log_request(request)

    # hack for testing purposes
    #user, _ = User.objects.get_or_create(id=17, username='LosKarlos')
    user=request.user

    task = practice_service.get_next_task(student=user)
    return JsonResponse(task)


@allow_lazy_user
def get_task_by_id(request, id):
    """Return response with requested task.
    """
    logger.log_request(request)
    try:
        task = practice_service.get_task_by_id(
                student=request.user,
                task_id=int(id))
        return JsonResponse(task)
    except LookupError:
        raise Http404('This task is not available.')


def post_attempt_report(request):
    """Store and process task result.

    POST params:
        task-instance-id: int,
        attempt: int, counted from 1,
        solved: bool,
        given-up: bool,
        time: int, number of seconds,
        flow-report:  0=unknown, 1=very_difficult, 2=difficult, 3=just_right, 4=easy

    Returns:
        task-instance-closed: true after the task is solved or given up
        earned-credits: int
    """
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    logger.log_request(request)
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    result = practice_service.process_attempt_report(student=request.user, report=data)
    return JsonResponse(result)

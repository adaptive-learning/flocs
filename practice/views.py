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
    """
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')

    logger.log_request(request)

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    # hack for testing purposes
    #user = User.objects.get(id=17)
    user=request.user

    practice_service.process_attempt_report(student=user, report=data)

    return HttpResponse('ok')

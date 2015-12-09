"""Access layer (controller) of practice app
"""

from common.logUtils import LoggingUtils
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from practice.services import practice_service
import json

logger = LoggingUtils()

def get_next_task(request):
    """Return response with next task.
    """
    logger.log_request(request)

    # hack for testing purposes
    #user, _ = User.objects.get_or_create(id=17, username='LosKarlos')
    user=request.user

    task = practice_service.get_next_task(student=user)
    return JsonResponse(task)


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

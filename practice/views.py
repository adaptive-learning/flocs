"""Access layer (controller) of practice app
"""

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from practice.services import practice_service
import json


def get_next_task(request):
    """Return response with next task.
    """
    # TODO: get current student, user=request.user ?
    # hack for testing purposes
    user, _ = User.objects.get_or_create(id=17, username='LosKarlos')

    task = practice_service.get_next_task(student=user)
    return JsonResponse(task)


def post_attempt_report(request):
    """Store and process task result.
    """
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    # TODO: get current student, user=request.user ?
    # hack for testing purposes
    user = User.objects.get(id=17)

    practice_service.process_attempt_report(student=user, report=data)

    return HttpResponse('ok')

"""Access layer (controller) of practice app
"""

from lazysignup.decorators import allow_lazy_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from django.http import Http404
import json

from common.logUtils import LoggingUtils
from practice.services import practice_service
from practice.services import details

logger = LoggingUtils()


@allow_lazy_user
def get_next_task(request):
    """Return response with next task for the current user.

    Returns:
        task-instance-id: int
        task: task object
        instructions: list of instructions
    """
    logger.log_request(request)
    user=request.user
    task = practice_service.get_next_task(student=user)
    return JsonResponse(task)


@allow_lazy_user
def get_task_by_id(request, id):
    """Return specific task for the current user.

    It's similar to api/practice/next-task/ except that it returns requested
    task, not a task chosen by the system. It's also similar to
    api/tasks/get-task/{taskId}, but adds user-specific informations, such as
    task instance ID and instructions.

    Returns:
        task-instance-id: int
        task : task object
        instructions: list of instructions
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
    """Store and process result of a single attempt

    POST params:
        task-instance-id: int,
        attempt: int, counted from 1,
        solved: bool,
        time: int, number of seconds,

    Returns:
        task-solved-first-time: bool
        earned-credits: int
    """
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    logger.log_request(request)
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    task_solved_first_time, credits = practice_service.process_attempt_report(
            student=request.user, report=data)
    response = {
        'task-solved-first-time': task_solved_first_time,
        'earned-credits': credits
    }
    return JsonResponse(response)


def post_giveup_report(request):
    """Process a report about user having given up a task

    POST params:
        task-instance-id: int,
        time: int, number of seconds,
    """
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    logger.log_request(request)
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    practice_service.process_giveup_report(
            student=request.user,
            task_instance_id=data['task-instance-id'],
            time_spent=data['time'])
    return HttpResponse('ok')


def post_flow_report(request):
    """Store and process flow_report after a task is solved.

    POST params:
        task-instance-id: int,
        flow-report:  0=unknown, 1=very_difficult, 2=difficult,
                      3=just_right, 4=easy
    """
    if request.method != "POST":
        return HttpResponseBadRequest('Has to be POST request.')
    logger.log_request(request)
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    result = practice_service.process_flow_report(
            student=request.user,
            task_instance_id=data['task-instance-id'],
            reported_flow=data.get('flow-report'))
    return HttpResponse('ok')


@login_required
def get_practice_details(request):
    """Get information about practice and skill of current user.

    Returns:
        - total-credits
        - free-credits
        - solved-tasks-count
    """
    print('jsem tady nebo ne')
    logger.log_request(request)
    practice_details = details.get_practice_details(user=request.user)
    details_dict = {
        'total-credits': practice_details.total_credits,
        'free-credits': practice_details.free_credits,
        'solved-tasks-count': practice_details.solved_tasks_count
    }
    return JsonResponse(details_dict)

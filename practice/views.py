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
from practice.services import practice_session_service
from practice.services import details
from practice.models.task_instance import FlowRating

logger = LoggingUtils()


@allow_lazy_user
def get_next_task_in_session(request):
    """Return response with next task for the current user.

    Returns:
        task-instance-id: int
        task: task object
        instructions: list of instructions
        session: session object
    """
    logger.log_request(request)
    user=request.user
    task_info = practice_service.get_next_task_in_session(user=user)
    task_dict = task_info_to_json(task_info)
    return JsonResponse(task_dict)


@allow_lazy_user
def get_task_by_id(request, id):
    """Return specific task for the current user.

    It's similar to api/practice/next-task/ except that it returns requested
    task, not a task chosen by the system. It's also similar to
    api/tasks/get-task/{taskId}, but adds user-specific informations, such as
    task instance ID and instructions.

    Returns:
        task-instance-id: int
        task: task object
        instructions: list of instructions
        session: session object
    """
    logger.log_request(request)
    try:
        task = practice_service.get_task_by_id(
                user=request.user,
                task_id=int(id))
        return JsonResponse(task_info_to_json(task))
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
    processing_result = practice_service.process_attempt_report(
            user=request.user, report=data)
    response = {
        'task-solved-first-time': processing_result.task_solved_first_time,
        'time': processing_result.time,
        'percentil': processing_result.percentil,
        'speed-bonus': processing_result.speed_bonus,
        'earned-credits': processing_result.credits,
        'progress': [progress_level_to_json(pl) for pl in processing_result.progress]
    }
    return JsonResponse(response)


def progress_level_to_json(progress_level):
    json_dict = {
        'level': progress_level.level,
        'credits-from': progress_level.credits_from,
        'credits-to': progress_level.credits_to,
        'max-credits': progress_level.max_credits,
        'blocks': [block_to_json(b) for b in progress_level.blocks],
    }
    return json_dict


def block_to_json(block):
    json_dict = {
        'name': block.name,
    }
    return json_dict


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
            user=request.user,
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
            user=request.user,
            task_instance_id=data['task-instance-id'],
            reported_flow=FlowRating.from_key(data.get('flow-report')))
    return HttpResponse('ok')


@login_required
def get_practice_details(request):
    """Get information about practice and skill of current user.

    Returns:
        - total-credits
        - free-credits
        - solved-tasks-count
    """
    logger.log_request(request)
    practice_details = details.get_practice_details(user=request.user)
    details_dict = {
        'total-credits': practice_details.total_credits,
        'free-credits': practice_details.free_credits,
        'solved-tasks-count': practice_details.solved_tasks_count,
        'available-blocks': [block.to_json() for block in
                             practice_details.available_blocks]
    }
    return JsonResponse(details_dict)


@allow_lazy_user
def get_session_overview(request):
    """
    Returns information about student's last session.

    Returns:
        task_instances: objects
    """
    logger.log_request(request)
    user=request.user
    session_overview = practice_service.get_session_overview(user)
    sess_overview_dict = session_overview_to_json(session_overview)
    return JsonResponse(sess_overview_dict)


def task_info_to_json(task_info):
    session_dict = None
    if task_info.session != None:
        task_instances = practice_session_service.get_all_task_instances(task_info.session)
        session_dict = {
            'task': task_info.session.task_counter,
            'max': practice_session_service.TASKS_IN_SESSION,
            'task-instances': [task_instance_to_json(task_instance)
                               for task_instance in task_instances]
        }
    task_dict = {
        'task-instance-id': task_info.task_instance.pk,
        'task': task_info.task.to_json(),
        'student-toolbox': [block.to_json() for block in task_info.student_toolbox],
        'new-instructions': instructions_to_json(task_info.new_instructions),
        'all-instructions': instructions_to_json(task_info.all_instructions),
        'session': session_dict
    }
    return task_dict


def task_instance_to_json(task_instance):
    task_instance_dict = {
        'task': task_instance.task.to_json(),
        'solved': task_instance.solved,
        'given-up': task_instance.given_up,
        'time-spent': task_instance.time_spent,
        'reported-flow': task_instance.reported_flow,
        'attempt-count': task_instance.attempt_count,
        'earned-credits': task_instance.earned_credits
    }
    return task_instance_dict


def session_overview_to_json(session_overview):
    sess_overview_dict = {
            'task-instances': list(map(task_instance_to_json, session_overview.task_instances)),
            'overall-time': session_overview.overall_time,
            'percentils': session_overview.percentils
            }
    return sess_overview_dict


def instructions_to_json(instructions):
    if instructions is None:
        return []
    return [instruction_to_json(instruction) for instruction in instructions]


def instruction_to_json(instruction):
    concept = instruction.concept
    instruction_dict = {
        'concept': concept.name,
        'type': concept.get_type(),
        'text': instruction.text,
    }
    if concept.get_type() == 'block':
        instruction_dict['blockKey'] = concept.blockconcept.block.identifier
    return instruction_dict

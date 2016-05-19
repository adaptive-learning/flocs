from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from stats.services.student_statistics import get_statistics_for_user


@login_required
def get_student_statistics(request):
    """ Return response with statistics for current user
    """
    statistics = get_statistics_for_user(user=request.user)
    statistics_dict = {
        'finished-tasks': [finished_task_to_json(t) for t in statistics.finished_tasks]
    }
    return JsonResponse(statistics_dict)


def finished_task_to_json(finished_task):
    finished_task_dict = {
      'title': finished_task.title,
      'credits': finished_task.credits,
      #'concepts': [concept.identifier for concept in finished_task.concepts],
      'concepts': [concept for concept in finished_task.concepts],
      'time': finished_task.time,
      'percentil': finished_task.percentil,
      'flow': finished_task.flow,
    }
    return finished_task_dict

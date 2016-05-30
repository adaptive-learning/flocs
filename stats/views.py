from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from stats.services.student_statistics import get_statistics_for_user


@login_required
def get_student_statistics(request):
    """ Return response with statistics for current user
    """
    statistics = get_statistics_for_user(user=request.user)
    statistics_dict = {
        'overview': overview_to_json(statistics.overview),
        'blocks': [block_to_json(b) for b in statistics.blocks],
        'finished-tasks': [finished_task_to_json(t) for t in statistics.finished_tasks],
    }
    return JsonResponse(statistics_dict)


def overview_to_json(overview):
    overview_dict = {
        'solved-count': overview.solved_count,
        'sessions-count': overview.sessions_count,
        'total-credits': overview.total_credits,
        'free-credits': overview.free_credits,
        'total-flow-time': overview.total_flow_time,
        'blocks-count': overview.blocks_count,
        'concepts-count': overview.concepts_count,
    }
    return overview_dict


def block_to_json(block):
    block_dict = {
        'identifier': block.identifier,
        'name': block.name,
        'level': block.level,
        'purchased': block.purchased,
        'active': block.active,
        'credits': block.credits,
        'credits-paid': block.credits_paid,
        'concept-stats': concept_stats_to_json(block.concept_stats),
    }
    return block_dict


def finished_task_to_json(finished_task):
    finished_task_dict = {
        'task-id': finished_task.task_id,
        'title': finished_task.title,
        'credits': finished_task.credits,
        'concepts': [concept.name for concept in finished_task.concepts],
        'time': finished_task.time,
        'percentil': finished_task.percentil,
        'flow': finished_task.flow,
    }
    return finished_task_dict


def concept_stats_to_json(concept):
    concept_stats_dict = {
        'identifier': concept.identifier,
        'solved-count': concept.solved_count,
        'mastered': concept.mastered,
    }
    return concept_stats_dict

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from stats.services.student_statistics import get_statistics_for_user
from stats.services import admin_statistics
from django.contrib.admin.views.decorators import staff_member_required


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

@staff_member_required
def get_admin_stats(request):
    """ Return response with the admin statistics
    """
    statistics = admin_statistics.get_admin_stats()
    statistics_dict = {
            'task_stats': [task_stat_to_json(task) for task in statistics.task_stats],
            'daily_stats': [daily_stat_to_json(day) for day in statistics.daily_stats],
            'block_stats': [block_stat_to_json(block) for block in statistics.block_stats],
            'concept_stats': [concept_stat_to_json(concept) for concept in statistics.concept_stats],
            'session_stats': session_stats_to_json(statistics.session_stats)
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

def task_stat_to_json(task_stat):
    task_stat_dict = {
            'id': task_stat.id,
            'title': task_stat.title,
            'solved_count': task_stat.solved_count,
            'time_median': task_stat.time_median,
            'attempts_median': task_stat.attempts_median,
            'concepts': [concept.name for concept in task_stat.concepts]
    }
    return task_stat_dict

def daily_stat_to_json(daily_stat):
    daily_stat_dict = {
            'date': daily_stat.date,
            'students': daily_stat.students,
            'solved_tasks': daily_stat.solved_tasks
    }
    return daily_stat_dict

def block_stat_to_json(block_stats):
    block_stat_dict = {
            'name': block_stats.name,
            'num_of_tasks': block_stats.num_of_tasks,
            'num_of_students': block_stats.num_of_students
    }
    return block_stat_dict

def concept_stat_to_json(concept_stat):
    concept_stat_dict = {
            'name': concept_stat.name,
            'type': concept_stat.type,
            'num_of_tasks': concept_stat.num_of_tasks,
            'num_of_students': concept_stat.num_of_students,
            'num_of_solved_tasks': concept_stat.num_of_solved_tasks
    }
    return concept_stat_dict

def session_stats_to_json(session_stats):
    session_stat_dict = {
            'length_median': session_stats.length_median,
            'solved_ratio': session_stats.solved_ratio,
            'unfinished': session_stats.unfinished
    }
    return session_stat_dict

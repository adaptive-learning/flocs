"""
Service provides admin statistics.
"""

from django.db.models import Count, Avg
from collections import namedtuple, Counter
from common.utils.math import median
from tasks.models import TaskModel
from practice.models import TaskInstanceModel, StudentModel, PracticeSession
from blocks.models import Block
from concepts.models import Concept

# Named Tuples for admin statistics
AdminStats = namedtuple('AdminStats', 
        ['task_stats', 'daily_stats', 'block_stats', 'concept_stats', 
            'session_stats'])
TaskStats = namedtuple('TaskStats', 
        ['id', 'title', 'solved_count', 'time_median', \
            'attempts_median', 'concepts']) 
DailyStats = namedtuple('DailyStats', 
        ['date', 'students', 'solved_tasks']) 
BlockStats = namedtuple('BlockStats',
        ['name', 'num_of_tasks', 'num_of_students'])
ConceptStats = namedtuple('ConceptStats',
        ['name', 'type', 'num_of_tasks', 'num_of_students', 'num_of_solved_tasks'])
SessionStats = namedtuple('SessionStats',
        ['length_median', 'solved_ratio', 'unfinished'])

def get_admin_stats():
    admin_stats = AdminStats(
            task_stats = get_tasks_stats(),
            daily_stats = get_daily_stats(),
            block_stats = get_block_stats(),
            concept_stats = get_concept_stats(),
            session_stats = get_session_stats())
    return admin_stats

def get_tasks_stats():
    tasks = TaskModel.objects.all()
    task_stats = []
    for task in tasks:
        task_stat = TaskStats(
                 id = task.pk,
                 title = task.title,
                 solved_count = TaskInstanceModel.objects.filter(
                     task=task, solved=True).count(),
                 time_median = get_time_median(task),
                 attempts_median = get_attempts_median(task),
                 #concepts = task.get_contained_concepts()) # allow later
                 concepts = task.get_programming_concepts())
        task_stats.append(task_stat)
    return task_stats

def get_daily_stats():
    instances_by_date = TaskInstanceModel.objects.filter(solved=True) \
            .extra({'date': "date(time_start)"}) \
            .values('date') \
            .annotate(tasks=Count('id')) \
            .annotate(students=(Count('student', distinct=True))) \
            .order_by('-date')
    daily_stats = []
    for day in instances_by_date:
        daily_stat = DailyStats(
                date = day['date'],
                students = day['students'],
                solved_tasks = day['tasks'])
        daily_stats.append(daily_stat)
    return daily_stats

def get_block_stats():
    block_stats = []
    for block in Block.objects.all():
        block_stat = BlockStats(
                name = block.name,
                num_of_tasks = get_num_of_tasks_for_block(block),
                num_of_students = get_num_of_students_for_block(block))
        block_stats.append(block_stat)
    return block_stats

def get_concept_stats():
    concept_stats = []
    num_of_tasks_for_concept = get_num_of_tasks_for_concepts()
    num_of_students_for_concept = get_num_of_students_for_concepts()
    num_of_solved_tasks_for_concept = get_num_of_solved_tasks_for_concepts()
    for concept in Concept.objects.all():
        concept_stat = ConceptStats(
                name = concept.name,
                type = concept.get_type(),
                num_of_tasks = num_of_tasks_for_concept[concept],
                num_of_students = num_of_students_for_concept[concept],
                num_of_solved_tasks = num_of_solved_tasks_for_concept[concept])
        concept_stats.append(concept_stat)
    return concept_stats

def get_session_stats():
    finished = PracticeSession.objects.filter(duration__gt=0)
    unfinished = PracticeSession.objects.filter(duration=0) # or expired
    return SessionStats(
            length_median = median([s.duration for s in finished]),
            solved_ratio = len(finished) / len(unfinished),
            unfinished = len(unfinished))


def get_time_median(task):
    times = TaskInstanceModel.objects.filter(task=task) \
            .values_list('time_spent', flat=True)
    return median(times)

def get_attempts_median(task):
    attempts = TaskInstanceModel.objects \
            .filter(task=task) \
            .values_list('attempt_count', flat=True)
    return median(attempts)

def get_num_of_tasks_for_block(block):
    return len([t for t in TaskModel.objects.all() if block in t.get_required_blocks()])

def get_num_of_students_for_block(block):
    return len([s for s in StudentModel.objects.all() if block in s.get_available_blocks()])

def get_num_of_tasks_for_concepts():
    counter = Counter()
    for task in TaskModel.objects.all():
        counter.update(task.get_contained_concepts())
    return counter

def get_num_of_students_for_concepts():
    counter = Counter()
    for student in StudentModel.objects.all():
        counter.update(student.get_seen_concepts())
    return counter

def get_num_of_solved_tasks_for_concepts():
    counter = Counter()
    for inst in TaskInstanceModel.objects.all():
        counter.update(inst.task.get_contained_concepts())
    return counter


from collections import namedtuple
from practice.models import StudentModel
from practice.services.task_instance_service import get_solved_distinct_tasks_count

from practice.models import StudentModel

PracticeDetails = namedtuple('PracticeDetails',
        ['total_credits', 'free_credits', 'solved_tasks_count'])

def get_practice_details(user):
    student = StudentModel.objects.get_or_create(user_id=user.pk)[0]
    practice_details = PracticeDetails(
        total_credits = student.total_credits,
        free_credits = student.free_credits,
        solved_tasks_count = len(get_solved_distinct_tasks_count(user)))
    return practice_details

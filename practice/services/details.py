from collections import namedtuple
from practice.models import StudentModel
from practice.models import StudentTaskInfoModel

PracticeDetails = namedtuple('PracticeDetails',
        ['total_credits', 'free_credits', 'solved_tasks_count'])

def get_practice_details(user):
    student = StudentModel.objects.get_or_create(user=user)[0]
    practice_details = PracticeDetails(
        total_credits = student.total_credits,
        free_credits = student.free_credits,
        solved_tasks_count = get_solved_tasks_count(student))
    return practice_details


def get_solved_tasks_count(student):
    all_student_tasks = StudentTaskInfoModel.objects.filter(student=student)
    solved_count = len([task for task in all_student_tasks if task.is_solved()])
    return solved_count

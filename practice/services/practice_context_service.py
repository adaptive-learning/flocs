from common.flow_factors import FlowFactors
from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import TasksDifficultyModel
from practice.models import StudentsSkillModel
from practice.models.practice_context import PracticeContext
from datetime import datetime


def generate_practice_context(student=None, task=None, time=None):
    """
    Return a new practice context for given student.
    If a student does not have any skills in DB yet, it will create them.

    Args:
        student: a student to include into practice context
            or None to include all students
        task: a task to include into practice context
            or None to include all tasks
        time (datetime.datetime): time of the practice
            or None to use current time
    """
    time = time if time is not None else datetime.now()

    practice_context = PracticeContext(time=time)

    #tasks = TaskModel.objects.all()
    if task is not None:
        task_difficulties = [TasksDifficultyModel.objects.get(task=task)]
    else:
        task_difficulties = TasksDifficultyModel.objects.all()

    for task_difficulty in task_difficulties:
        task_id = task_difficulty.task.id
        for key, value in task_difficulty.get_difficulty_dict().items():
            practice_context.set(key, task=task_id, value=value)

    if student is not None:
        student_skill, _ = StudentsSkillModel.objects.get_or_create(student=student)
        student_skills = [student_skill]
    else:
        student_skills = StudentsSkillModel.objects.all()

    for student_skill in student_skills:
        for key, value in student_skill.get_skill_dict().items():
            practice_context.set(key, student=student.id, value=value)

    # TODO: load last attempt time

    return practice_context

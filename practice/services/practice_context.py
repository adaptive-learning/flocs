from common.flow_factors import FlowFactors
from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import TasksDifficultyModel
from practice.models import StudentsSkillModel

#from collections import defaultdict
from datetime import datetime


def generate_practice_context(student, time=None):
    """
    Return a new practice context for given student.
    """
    time = time if time is not None else datetime.now()

    practice_context = PracticeContext(time=time)

    #tasks = TaskModel.objects.all()
    for task_difficulty in TasksDifficultyModel.objects.all():
        task_id = task_difficulty.task.id
        for key, value in task_difficulty.get_difficulty_dict().items():
            practice_context.set(key, task=task_id, value=value)

    student_skill = StudentsSkillModel.objects.get(student=student)
    for key, value in student_skill.get_skill_dict().items():
        practice_context.set(key, student=student.id, value=value)

    # TODO: load last attempt time

    return practice_context


class PracticeContext(object):
    """
    Represenatation of a practice context parameters.
    """

    def __init__(self, parameters=[], **kwargs):
        """
        Initialize a new practice context.
        """
        self._parameters = dict()
        for name, student, task, value in parameters:
            self.set(name, student, task, value)
        for name, value in kwargs.items():
            self.set(name, value=value)

    def get_time(self):
        """
        Return time of the practice.
        """
        return self.get('time')

    def get_last_attempt_time(self, student, task):
        """
        Return a last time when the student attempted to solve the task.
        """
        return self.get('last-time', student, task)

    def get_skill_dict(self, student):
        """
        Return skill dictionary for given student
        """
        skill_dict = {}
        for student_factor in FlowFactors.student_factors():
            skill_dict[student_factor] = self.get(student_factor, student=student)
        return skill_dict

    def get_difficulty_dict(self, task):
        """
        Return difficulty dictionary for given task
        """
        difficulty_dict = {}
        for task_factor in FlowFactors.task_factors():
            difficulty_dict[task_factor] = self.get(task_factor, task=task)
        return difficulty_dict

    def get(self, parameter_name, student=None, task=None):
        """
        Return a parameter with given name and optionally for specified student
        and task.

        Args:
            parameter_name (string): name of a parameter to get
            student (int): ID of a student
            task (int): ID of a task
        Return:
            value of requested parameter (or list of values)
        """
        return self._parameters[(parameter_name, student, task)]

    def set(self, parameter_name, student=None, task=None, value=None):
        """
        Set a new value for a parameter.

        Args:
            parameter_name (string): name of a parameter to get
            student (int): ID of a student
            task (int): ID of a task
            value: value to set
        """
        self._parameters[(parameter_name, student, task)] = value

from common.flow_factors import FlowFactors
from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import TasksDifficultyModel
from practice.models import StudentsSkillModel
from datetime import datetime
#from .practice_context_manager import PracticeContextManager

# NOTE: Now, for simplicity, we use a factory function to generate a context,
# but in future, we may want to create a manager for the practice context.
# In such case, the entity class should probably depend on the manager (that is
# the Django way) and not vice versa.
# Instead of calling create_practice_context(), one would then use
# PracticeContext.objects.create().
def create_practice_context(student=None, task=None, time=None):
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

    #practice_context = self.model(time=time)
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
        practice_context.set('solution-count', task=task_id,
                value=task_difficulty.solution_count)

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


class PracticeContext(object):
    """
    Represenatation of a practice context parameters.
    """
    #objects = PracticeContextManager()

    def __init__(self, parameters=[], **kwargs):
        """
        Initialize a new practice context.
        """
        self._parameters = dict()
        self._task_ids = set()
        self._student_ids = set()
        for name, student, task, value in parameters:
            self.set(name, student, task, value)
        for name, value in kwargs.items():
            self.set(name, value=value)

    def get_all_task_ids(self):
        """
        Return list of IDs of all tasks in the context.
        """
        return list(self._task_ids)

    def get_all_student_ids(self):
        """
        Return list of IDs of all students in the context.
        """
        return list(self._student_ids)

    def get_time(self):
        """
        Return time of the practice.
        """
        return self.get('time')

    def get_solution_count(self, task):
        return self.get('solution-count', task=task)

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
        if task:
            self._task_ids.add(task)
        if student:
            self._student_ids.add(student)

    def update(self, parameter_name, student=None, task=None, update=None):
        assert update is not None
        old_value = self._parameters[(parameter_name, student, task)]
        new_value = update(old_value)
        self._parameters[(parameter_name, student, task)] = new_value


    def save(self):
        """Save changes in the practice context to DB
        """
        # NOTE: this is quite ugly ad-hoc solution and we should definitely
        # change the underlaying model for parameters to be more flexible
        for task in self.get_all_task_ids():
            task_difficulty = TasksDifficultyModel.objects.get(task_id=task)
            task_difficulty.programming = self.get(FlowFactors.TASK_BIAS, task=task)
            task_difficulty.solution_count = self.get_solution_count(task=task)
            task_difficulty.save()
        for student in self.get_all_student_ids():
            student_skill = StudentsSkillModel.objects.get(student_id=student)
            student_skill.programming = self.get(FlowFactors.STUDENT_BIAS, student=student)
            student_skill.conditions = self.get(FlowFactors.CONDITIONS, student=student)
            student_skill.loops = self.get(FlowFactors.LOOPS, student=student)
            student_skill.logic_expr = self.get(FlowFactors.LOGIC_EXPR, student=student)
            student_skill.colors = self.get(FlowFactors.COLORS, student=student)
            student_skill.tokens = self.get(FlowFactors.TOKENS, student=student)
            student_skill.pits = self.get(FlowFactors.PITS, student=student)
            student_skill.save()

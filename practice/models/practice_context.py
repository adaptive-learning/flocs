from django.core.exceptions import ObjectDoesNotExist
from common.flow_factors import FlowFactors
from tasks.models import TaskModel
from practice.models import StudentModel
from practice.models import StudentTaskInfoModel
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

    Args:
        student: a student to include into practice context
            or None to include all students
        task: a task to include into practice context
            or None to include all tasks
        time (datetime.datetime): time of the practice
            or None to use current time
    """
    # NOTE: massive refactoring -> temporarily return empty practice context
    # (for the original version, see version control)
    practice_context = PracticeContext()
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
        old_value = self.get(parameter_name, student, task)
        new_value = update(old_value)
        #self._parameters[(parameter_name, student, task)] = new_value
        self.set(parameter_name, student, task, new_value)

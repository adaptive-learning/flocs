"""Unit test of task instance model.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import StudentModel
from .task_instance import TaskInstanceModel

class TaskInstanceModelTest(TestCase):

    def test_create_task_instance(self):
        user = User.objects.create()
        student = StudentModel.objects.create(user=user)
        task = TaskModel.objects.create()
        task_instance = TaskInstanceModel(
            student=student,
            task=task)
        self.assertEquals(task_instance.attempt_count, 0)
        self.assertEquals(task_instance.solved, False)
        self.assertEquals(task_instance.given_up, False)
        self.assertEquals(task_instance.is_completed(), False)
        self.assertEquals(task_instance.reported_flow, 0)

    def test_update_after_unsuccessful_attempt(self):
        task_instance = TaskInstanceModel()
        task_instance.update_after_attempt(attempt_count=4, time=30, solved=False)
        self.assertEquals(task_instance.attempt_count, 4)
        self.assertEquals(task_instance.time_spent, 30)
        self.assertEquals(task_instance.solved, False)
        self.assertEquals(task_instance.is_completed(), False)
        self.assertEquals(task_instance.reported_flow, 0)

    def test_update_after_successful_attempt(self):
        task_instance = TaskInstanceModel()
        task_instance.update_after_attempt(attempt_count=5, time=36, solved=True)
        self.assertEquals(task_instance.attempt_count, 5)
        self.assertEquals(task_instance.time_spent, 36)
        self.assertEquals(task_instance.solved, True)
        self.assertEquals(task_instance.is_completed(), True)
        self.assertEquals(task_instance.reported_flow, 0)

    def test_update_after_giveup(self):
        task_instance = TaskInstanceModel()
        task_instance.update_after_giveup(time_spent=36)
        self.assertEquals(task_instance.attempt_count, 0)
        self.assertEquals(task_instance.time_spent, 36)
        self.assertEquals(task_instance.solved, False)
        self.assertEquals(task_instance.given_up, True)
        self.assertEquals(task_instance.is_completed(), True)

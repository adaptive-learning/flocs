"""Unit test of task service
"""

from django.contrib.auth.models import User
from django.test import TestCase
from tasks.models import TaskModel
from practice.models import TasksDifficultyModel
from . import practice_service


class PracticeServiceTest(TestCase):

    def setUp(self):
        self.student = User.objects.create()

    def test_get_next_task(self):
        stored_task = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        TasksDifficultyModel.objects.create(task=stored_task)
        retrieved_task = practice_service.get_next_task(student=self.student)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(stored_task.to_json(), retrieved_task)

    def test_no_task_available(self):
        # if there are no tasks available, task_servise should raise
        # LookupError
        self.assertRaises(LookupError,
                practice_service.get_next_task, self.student)

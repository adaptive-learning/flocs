"""Unit test of task service
"""

from django.test import TestCase
from tasks.models import TaskModel
from . import practice_service


class PracticeServiceTest(TestCase):

    pass
    #def test_get_next_task(self):
    #    stored_task = TaskModel.objects.create(maze_settings="{}",
    #            workspace_settings='{"foo": "bar"}')
    #    retrieved_task = practice_service.get_next_task(student=self.FAKE_STUDENT)
    #    self.assertIsNotNone(retrieved_task)
    #    self.assertEqual(stored_task.to_json(), retrieved_task)

    #def test_no_task_available(self):
    #    # if there are no tasks available, task_servise should raise
    #    # LookupError
    #    self.assertRaises(LookupError, practice_service.get_next_task, None)

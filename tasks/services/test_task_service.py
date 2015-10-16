"""Unit test of task service
"""

from django.test import TestCase
from tasks.models import TaskModel
from . import task_service


class TaskServiceTest(TestCase):

    # Testing get_all_tasks()

    def test_get_all_tasks(self):
        task1 = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        task2 = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo2": "bar2"}')
        retrieved_tasks = task_service.get_all_tasks()
        self.assertIsNotNone(retrieved_tasks)
        self.assertEqual(len(retrieved_tasks), 2)


    # Testing get_task_by_id(request_id)

    def test_no_task_available(self):
        # if there are no tasks available, task_servise should raise
        # LookupError
        self.assertRaises(LookupError, task_service.get_task_by_id, 1)


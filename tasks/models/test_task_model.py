"""Unit test of task model
"""

from django.test import TestCase
from .task import TaskModel


class TaskModelTest(TestCase):

    def test_to_json(self):
        task = TaskModel(
                maze_settings='{"foo1": "bar1"}',
                workspace_settings='{"foo2": "bar2"}')
        task_json = task.to_json()
        self.assertIn('maze-settings', task_json)
        self.assertIn('workspace-settings', task_json)
        self.assertEquals(task_json['maze-settings'], {'foo1': 'bar1'})
        self.assertEquals(task_json['workspace-settings'], {'foo2': 'bar2'})

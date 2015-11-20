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

    def test_process_attempt_report(self):
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, solution_count=5)
        report = {
            "task-id": 1,
            "attempt": 5,
            "result": {
                "solved": True,
                "time": 23456
            },
            "flow-report": 1
        }
        practice_service.process_attempt_report(self.student, report)
        difficulty = TasksDifficultyModel.objects.get(task_id=1)
        self.assertEquals(6, difficulty.solution_count)
        # TODO: check that the difficulty and skill parameters were changed in
        # DB

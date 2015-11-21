"""Unit test of task service
"""

from django.contrib.auth.models import User
from django.test import TestCase
from tasks.models import TaskModel
from practice.models import TasksDifficultyModel
from practice.models import TaskInstanceModel
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
        self.assertEquals({"foo": "bar"}, retrieved_task['task']['workspace-settings'])
        self.assertEquals({}, retrieved_task['task']['maze-settings'])
        self.assertEquals(TaskInstanceModel.objects.first().id,
                retrieved_task['task-instance-id'])

    def test_no_task_available(self):
        # if there are no tasks available, task_servise should raise
        # LookupError
        self.assertRaises(LookupError,
                practice_service.get_next_task, self.student)

    def test_process_attempt_report(self):
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, solution_count=5)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=self.student,
                predicted_flow=0.22)
        report = {
            "task-instance-id": 1,
            "task-id": 1,
            "attempt": 7,
            "solved": True,
            "time": 234,
            "flow-report": 1
        }
        practice_service.process_attempt_report(self.student, report)
        difficulty = TasksDifficultyModel.objects.get(task_id=1)
        self.assertEquals(6, difficulty.solution_count)
        task_instance = TaskInstanceModel.objects.get(id=1)
        self.assertAlmostEquals(0.22, task_instance.predicted_flow)
        self.assertEquals(7, task_instance.attempt_count)
        self.assertEquals(234, task_instance.time_spent)
        # TODO: check that the difficulty and skill parameters were changed in
        # DB

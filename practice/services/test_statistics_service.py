"""Unit test of statistics service
"""

from django.test import TestCase

from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import StudentModel
from practice.models import TaskInstanceModel
from . import statistics_service


class StatisticServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(user=self.user)

    def test_percentil(self):
        task = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        TaskInstanceModel.objects.create(task=task, student=self.student,
                predicted_flow=0.22, time_spent=20, solved=True)
        TaskInstanceModel.objects.create(task=task, student=self.student,
                predicted_flow=0.22, time_spent=21, solved=True)
        ti3 = TaskInstanceModel.objects.create(task=task, student=self.student,
                predicted_flow=0.22, time_spent=15, solved=True)
        percentil = statistics_service.percentil(ti3)
        self.assertEquals(percentil, 100)
        TaskInstanceModel.objects.create(task=task, student=self.student,
                predicted_flow=0.22, time_spent=10, solved=True)
        ti5 = TaskInstanceModel.objects.create(task=task, student=self.student,
                predicted_flow=0.22, time_spent=15, solved=True)
        percentil = statistics_service.percentil(ti5)
        self.assertEquals(percentil, 80)


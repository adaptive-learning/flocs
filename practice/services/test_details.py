from django.contrib.auth.models import User
from django.test import TestCase
from tasks.models import TaskModel
from practice.models import StudentModel
from practice.models import TaskInstanceModel
from practice.services import details


class DetailsServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(user=self.user)
        TaskModel.objects.create(id=1)
        TaskModel.objects.create(id=2)
        TaskModel.objects.create(id=3)

    def test_get_practice_details_no_solved_tasks(self):
        self.student.total_credits = 7
        self.student.free_credits = 3
        self.student.save()
        practice_details = details.get_practice_details(self.user)
        self.assertEqual(practice_details.total_credits, 7)
        self.assertEqual(practice_details.free_credits, 3)
        self.assertEqual(practice_details.solved_tasks_count, 0)

    def test_get_practice_details_with_solved_tasks(self):
        TaskInstanceModel.objects.create(task_id=1, student=self.user, solved=True)
        TaskInstanceModel.objects.create(task_id=1, student=self.user, solved=True)
        TaskInstanceModel.objects.create(task_id=2, student=self.user, solved=True)
        TaskInstanceModel.objects.create(task_id=3, student=self.user, solved=False)
        practice_details = details.get_practice_details(self.user)
        self.assertEqual(practice_details.total_credits, 0)
        self.assertEqual(practice_details.free_credits, 0)
        self.assertEqual(practice_details.solved_tasks_count, 2)

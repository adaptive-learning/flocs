from django.contrib.auth.models import User
from django.test import TestCase
from tasks.models import TaskModel
from practice.models import StudentModel
from practice.models import StudentTaskInfoModel
from practice.models import TaskInstanceModel
from practice.services import details
from blocks.models import BlockModel

class DetailsServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(user=self.user)
        self.task1 = TaskModel.objects.create(id=1)
        self.task2 = TaskModel.objects.create(id=2)
        self.task3 = TaskModel.objects.create(id=3)
        BlockModel.objects.create(id=1, name="foo", identifiers="bar")

    def test_get_practice_details_no_solved_tasks(self):
        self.student.total_credits = 7
        self.student.free_credits = 3
        self.student.save()
        practice_details = details.get_practice_details(self.user)
        self.assertEqual(practice_details.total_credits, 7)
        self.assertEqual(practice_details.free_credits, 3)
        self.assertEqual(practice_details.solved_tasks_count, 0)

    def test_get_practice_details_with_solved_tasks(self):
        instance1 = TaskInstanceModel.objects.create(task_id=1, student=self.student, solved=True)
        instance2 = TaskInstanceModel.objects.create(task_id=1, student=self.student, solved=True)
        instance3 = TaskInstanceModel.objects.create(task_id=2, student=self.student, solved=True)
        instance4 = TaskInstanceModel.objects.create(task_id=3, student=self.student, solved=False)
        info1 = StudentTaskInfoModel.objects.create(student=self.student, task=self.task1)
        info2 = StudentTaskInfoModel.objects.create(student=self.student, task=self.task2)
        info3 = StudentTaskInfoModel.objects.create(student=self.student, task=self.task3)
        info1.update(instance1)
        info1.update(instance2)
        info2.update(instance3)
        info3.update(instance4)
        info1.save()
        info2.save()
        info3.save()
        practice_details = details.get_practice_details(self.user)
        self.assertEqual(practice_details.total_credits, 0)
        self.assertEqual(practice_details.free_credits, 0)
        self.assertEqual(practice_details.solved_tasks_count, 2)

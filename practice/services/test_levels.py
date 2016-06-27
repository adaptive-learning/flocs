from django.contrib.auth.models import User
from django.test import TestCase
from blocks.models import Toolbox
from practice.models import StudentModel
from .levels import level_progress


class LevelsServiceTest(TestCase):

    def setUp(self):
        self.toolbox1 = Toolbox.objects.create(name='first', level=1, credits=5)
        self.toolbox2 = Toolbox.objects.create(name='second', level=2, credits=10)
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(
                user=self.user,
                total_credits=50,
                toolbox=self.toolbox1)

    def test_try_levelup_with_success(self):
        self.student.free_credits = 0
        progress = level_progress(self.student, 11)
        self.assertEqual(len(progress), 2)
        self.assertEqual(self.student.toolbox, self.toolbox2)
        self.assertEqual(self.student.free_credits, 1)
        self.assertEqual(self.student.total_credits, 61)

    def test_try_levelup_already_having_some_credits(self):
        self.student.free_credits = 5
        progress = level_progress(self.student, 6)
        self.assertEqual(len(progress), 2)
        self.assertEqual(self.student.toolbox, self.toolbox2)
        self.assertEqual(self.student.free_credits, 1)
        self.assertEqual(self.student.total_credits, 56)

    def test_try_levelup_spending_all_credits(self):
        self.student.free_credits = 0
        progress = level_progress(self.student, 10)
        self.assertEqual(len(progress), 2)
        self.assertEqual(self.student.toolbox, self.toolbox2)
        self.assertEqual(self.student.free_credits, 0)
        self.assertEqual(self.student.total_credits, 60)

    def test_try_levelup_db_changed(self):
        self.student.free_credits = 0
        progress = level_progress(self.student, 11)
        retrieved_student = StudentModel.objects.get(pk=self.student.pk)
        self.assertEqual(retrieved_student.toolbox, self.toolbox2)
        self.assertEqual(retrieved_student.free_credits, 1)
        self.assertEqual(retrieved_student.total_credits, 61)

    def test_no_levelup(self):
        self.student.free_credits = 0
        progress = level_progress(self.student, 9)
        self.assertEqual(len(progress), 1)
        self.assertEqual(self.student.toolbox, self.toolbox1)
        self.assertEqual(self.student.free_credits, 9)
        self.assertEqual(self.student.total_credits, 59)

    def test_try_levelup_maximum_level(self):
        self.student.free_credits = 0
        self.student.toolbox = self.toolbox2
        progress = level_progress(self.student, 40)
        self.assertEqual(len(progress), 1)
        self.assertEqual(self.student.toolbox, self.toolbox2)
        self.assertEqual(self.student.free_credits, 40)
        self.assertEqual(self.student.total_credits, 90)

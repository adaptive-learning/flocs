"""Unit test of students skill model
"""

from django.test import TestCase
from practice.models import StudentModel
from common.flow_factors import FlowFactors
from decimal import Decimal

from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import TasksDifficultyModel
from practice.core.task_selection import ScoreTaskSelector as TaskSelector
from practice.models.practice_context import create_practice_context

class StudentModelTest(TestCase):

    def test_get_skill_dict(self):
        students_skills = StudentModel(
                programming=Decimal('0.14'),
                conditions=0,
                loops=0.5,
                logic_expr=-0.5,
                colors=0,
                tokens=0,
                pits=0,
                )
        student_vector = students_skills.get_skill_dict()
        self.assertAlmostEquals(0.14, student_vector[FlowFactors.STUDENT_BIAS])
        self.assertAlmostEquals(0, student_vector[FlowFactors.CONDITIONS])
        self.assertAlmostEquals(0.5, student_vector[FlowFactors.LOOPS])
        self.assertAlmostEquals(-0.5, student_vector[FlowFactors.LOGIC_EXPR])
        self.assertAlmostEquals(0, student_vector[FlowFactors.COLORS])
        self.assertAlmostEquals(0, student_vector[FlowFactors.TOKENS])
        self.assertAlmostEquals(0, student_vector[FlowFactors.PITS])

    def test_initial_skill(self):
        """
        This test should prove that bias of the new student is initialized well.
        The first task should be the easiest one.
        """
        # create user
        user = User.objects.create()
        # create tasks
        task1 = TaskModel.objects.create()
        task2 = TaskModel.objects.create()
        # simple task with few factors
        task_dif_1 = TasksDifficultyModel(
                task=task1,
                programming=Decimal('-0.59'),
                conditions=False,
                loops=True,
                logic_expr=False,
                colors=True,
                tokens=False,
                pits=False,
                )
        # difficult task with few factors
        task_dif_1 = TasksDifficultyModel(
                task=task1,
                programming=Decimal('-0.58'),
                conditions=False,
                loops=True,
                logic_expr=False,
                colors=True,
                tokens=False,
                pits=False,
                )
        # easier task but with more factors
        task_dif_2 = TasksDifficultyModel(
                task=task2,
                programming=Decimal('-0.59'),
                conditions=True,
                loops=True,
                logic_expr=False,
                colors=True,
                tokens=False,
                pits=False,
                )
        task_dif_1.save()
        task_dif_2.save()
        student = StudentModel.objects.create(user=user)
        task_selector = TaskSelector()
        # create practice context
        practice_context = create_practice_context(user=user)
        # select task
        task_ids = [task1.id, task2.id]
        task_id = task_selector.select(task_ids, user.id, practice_context)
        # assert the selected task
        self.assertEquals(task_id, 1)


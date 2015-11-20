"""Unit test for practice context service.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import TasksDifficultyModel
from practice.models import StudentsSkillModel
from common.flow_factors import FlowFactors
from decimal import Decimal
from datetime import datetime

#from .practice_context_manager import PracticeContextManager
from .practice_context import create_practice_context


class PracticeContextManagerTest(TestCase):

    def test_generate_practice_context_with_student_and_time(self):
        task = TaskModel.objects.create()
        difficulty = TasksDifficultyModel.objects.create(
                task=task,
                programming=Decimal('-0.58'),
                conditions=False,
                loops=True,
                logic_expr=False,
                colors=False,
                tokens=False,
                pits=False,
        )
        student = User.objects.create()
        students_skills = StudentsSkillModel.objects.create(
                student=student,
                programming=Decimal('0.14'),
                conditions=0,
                loops=0.5,
                logic_expr=-0.5,
                colors=0,
                tokens=0,
                pits=0,
        )
        time = datetime(2015, 1, 2, 3, 4, 5)
        context = create_practice_context(student, time=time)
        #print(context._parameters)
        self.assertAlmostEquals(-0.58,
            context.get(FlowFactors.TASK_BIAS, task=task.id))
        self.assertAlmostEquals(0.5,
            context.get(FlowFactors.LOOPS, student=student.id))
        self.assertEquals(time, context.get_time())

    def test_generate_practice_context_with_student_and_task(self):
        task1 = TaskModel.objects.create()
        task2 = TaskModel.objects.create()
        difficulty1 = TasksDifficultyModel.objects.create(task=task1)
        difficulty2 = TasksDifficultyModel.objects.create(task=task2)
        student = User.objects.create()
        context = create_practice_context(student=student, task=task1)
        self.assertEquals([task1.id], context.get_all_task_ids())

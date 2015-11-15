"""Unit test of task difficulty model
"""

from django.test import TestCase
from .tasks_difficulty import TasksDifficultyModel, CONCEPT_WEIGHT
from decimal import Decimal

class TasksDifficultyModelTest(TestCase):
    def test_to_vector(self):
        task_difficulties = TasksDifficultyModel(
                programming=Decimal('-0.58'),
                conditions=False,
                loops=True,
                logic_expr=False,
                colors=False,
                tokens=False,
                pits=False,
                )
        task_vector = task_difficulties.to_vector()
        self.assertAlmostEquals(-0.58, task_vector[0])
        self.assertEquals(0, task_vector[1])
        self.assertEquals(CONCEPT_WEIGHT, task_vector[2])
        self.assertEquals(0, task_vector[3])
        self.assertEquals(0, task_vector[4])
        self.assertEquals(0, task_vector[5])
        self.assertEquals(0, task_vector[6])

    def test_number_of_concepts(self):
        task_difficulties = TasksDifficultyModel(
                programming=Decimal('-0.58'),
                conditions=False,
                loops=True,
                logic_expr=False,
                colors=True,
                tokens=False,
                pits=False,
                )
        num = task_difficulties.number_of_concepts()
        self.assertEquals(2, num)


"""Unit test of task difficulty model
"""

from django.test import TestCase
from common.flow_factors import FlowFactors
from decimal import Decimal
from .tasks_difficulty import TasksDifficultyModel, CONCEPT_WEIGHT

class TasksDifficultyModelTest(TestCase):
    def test_get_difficulty_dict(self):
        task_difficulties = TasksDifficultyModel(
                programming=Decimal('-0.58'),
                conditions=False,
                loops=True,
                logic_expr=False,
                colors=False,
                tokens=False,
                pits=False,
                )
        task_vector = task_difficulties.get_difficulty_dict()
        self.assertAlmostEquals(-0.58, task_vector[FlowFactors.TASK_BIAS])
        self.assertEquals(0, task_vector[FlowFactors.CONDITIONS])
        self.assertEquals(CONCEPT_WEIGHT, task_vector[FlowFactors.LOOPS])
        self.assertEquals(0, task_vector[FlowFactors.LOGIC_EXPR])
        self.assertEquals(0, task_vector[FlowFactors.COLORS])
        self.assertEquals(0, task_vector[FlowFactors.TOKENS])
        self.assertEquals(0, task_vector[FlowFactors.PITS])
        self.assertEquals(0, task_difficulties.solution_count)

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


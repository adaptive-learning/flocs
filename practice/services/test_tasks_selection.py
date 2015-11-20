"""Unit test for task selection modul.
"""

from datetime import datetime
from django.test import TestCase
from common.flow_factors import FlowFactors
from common.utils.activation import AMPLITUDE
from practice.models.practice_context import PracticeContext
from .task_selection import ScoreTaskSelector


class ScoreTaskSelectorTest(TestCase):

    def test_select_single(self):
        # mock practice context
        context = PracticeContext()
        context.get_difficulty_dict = lambda x: {FlowFactors.TASK_BIAS: 0}
        context.get_skill_dict = lambda x: {FlowFactors.STUDENT_BIAS: 0}

        selector = ScoreTaskSelector()
        result = selector.select([12], student_id=11, practice_context=context)
        self.assertEqual(12, result)

    def test_select_best(self):
        # mock practice context
        context = PracticeContext()
        context.get_difficulty_dict = lambda x: {FlowFactors.TASK_BIAS: 0.4}\
                if x == 5 else {FlowFactors.TASK_BIAS: 0.3}
        context.get_skill_dict = lambda x: {FlowFactors.STUDENT_BIAS: 0.5}

        selector = ScoreTaskSelector()
        result = selector.select([i for i in range(20)], student_id=11,
                practice_context=context)
        self.assertEqual(5, result)

    def test_score_flow(self):
        self.assertAlmostEquals(0, ScoreTaskSelector()._score_flow(0))
        self.assertLess(ScoreTaskSelector()._score_flow(0.1), 0)
        self.assertLess(ScoreTaskSelector()._score_flow(-0.1), 0)
        self.assertAlmostEquals(-1, ScoreTaskSelector()._score_flow(AMPLITUDE))

    def test_score_time(self):
        date1 = datetime(2015, 1, 1, 0, 0, 0)
        date2 = datetime(2015, 1, 1, 0, 1, 0)
        date3 = datetime(2015, 2, 1, 0, 0, 0)
        self.assertAlmostEquals(0,
            ScoreTaskSelector()._score_time_since_last_attempt(None, date1))
        self.assertAlmostEquals(-1,
            ScoreTaskSelector()._score_time_since_last_attempt(date1, date1))
        self.assertAlmostEqual(-0.95,
            ScoreTaskSelector()._score_time_since_last_attempt(date1, date2),
            delta=0.045)
        self.assertAlmostEqual(0,
            ScoreTaskSelector()._score_time_since_last_attempt(date1, date3))

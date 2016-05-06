from datetime import datetime
from django.test import TestCase
from common.flow_factors import FlowFactors
from common.utils.activation import AMPLITUDE
from practice.models.practice_context import PracticeContext
from practice.core.scores import flow_to_score, times_to_score


class ScoresTest(TestCase):

    def test_time_to_score(self):
        date1 = datetime(2015, 1, 1, 0, 0, 0)
        date2 = datetime(2015, 1, 1, 0, 12, 0)
        date3 = datetime(2015, 1, 5, 0, 0, 0)
        date4 = datetime(2015, 2, 1, 0, 0, 0)
        self.assertAlmostEquals(1, times_to_score(None, date1))
        self.assertAlmostEquals(0, times_to_score(date1, date1))
        self.assertAlmostEquals(0.05, times_to_score(date1, date2), delta=0.045)
        self.assertAlmostEquals(0.9, times_to_score(date1, date3), delta=0.1)
        self.assertAlmostEquals(1, times_to_score(date1, date4))

    def test_flow_to_score(self):
        self.assertAlmostEquals(flow_to_score(0), 1)
        self.assertLess(flow_to_score(0.1), 1)
        self.assertLess(flow_to_score(-0.1), 1)
        self.assertAlmostEquals(flow_to_score(AMPLITUDE), 0)

"""Unit test for flow prediction modul.
"""

from django.test import TestCase
from decimal import Decimal

from common.flow_factors import FlowFactors
from common.utils.activation import activation
from practice.models.practice_context import PracticeContext
from .flow_prediction import predict_flow


class FlowPredictionTest(TestCase):

    def test_predict_zero_flow(self):
        context = PracticeContext([
            (FlowFactors.STUDENT_BIAS,  11, None, 0),
            (FlowFactors.CONDITIONS,    11, None, 0),
            (FlowFactors.LOOPS,         11, None, 0),
            (FlowFactors.LOGIC_EXPR,    11, None, 0),
            (FlowFactors.COLORS,        11, None, 0),
            (FlowFactors.TOKENS,        11, None, 0),
            (FlowFactors.PITS,          11, None, 0),
            (FlowFactors.TASK_BIAS,     None, 12, 0),
            (FlowFactors.CONDITIONS,    None, 12, 0),
            (FlowFactors.LOOPS,         None, 12, 0),
            (FlowFactors.LOGIC_EXPR,    None, 12, 0),
            (FlowFactors.COLORS,        None, 12, 0),
            (FlowFactors.TOKENS,        None, 12, 0),
            (FlowFactors.PITS,          None, 12, 0)
        ])
        result = predict_flow(student_id=11, task_id=12, practice_context=context)
        self.assertAlmostEquals(0, result)


    def test_predict_flow1(self):
        context = PracticeContext([
            (FlowFactors.STUDENT_BIAS,  11, None, 5.2),
            (FlowFactors.CONDITIONS,    11, None, 0),
            (FlowFactors.LOOPS,         11, None, 0),
            (FlowFactors.LOGIC_EXPR,    11, None, 0),
            (FlowFactors.COLORS,        11, None, 0),
            (FlowFactors.TOKENS,        11, None, 0),
            (FlowFactors.PITS,          11, None, 0),
            (FlowFactors.TASK_BIAS,     None, 12, 3.7),
            (FlowFactors.CONDITIONS,    None, 12, 0),
            (FlowFactors.LOOPS,         None, 12, 0),
            (FlowFactors.LOGIC_EXPR,    None, 12, 0),
            (FlowFactors.COLORS,        None, 12, 0),
            (FlowFactors.TOKENS,        None, 12, 0),
            (FlowFactors.PITS,          None, 12, 0)
        ])
        result = predict_flow(student_id=11, task_id=12, practice_context=context)
        self.assertAlmostEquals(activation(1.5), result)

    def test_predict_flow2(self):
        context = PracticeContext([
            (FlowFactors.STUDENT_BIAS,  11, None, 5.2),
            (FlowFactors.CONDITIONS,    11, None, 0),
            (FlowFactors.LOOPS,         11, None, 1.2),
            (FlowFactors.LOGIC_EXPR,    11, None, 0),
            (FlowFactors.COLORS,        11, None, 0),
            (FlowFactors.TOKENS,        11, None, 0),
            (FlowFactors.PITS,          11, None, -0.1),
            (FlowFactors.TASK_BIAS,     None, 12, 3.7),
            (FlowFactors.CONDITIONS,    None, 12, 0),
            (FlowFactors.LOOPS,         None, 12, 0.5),
            (FlowFactors.LOGIC_EXPR,    None, 12, 0),
            (FlowFactors.COLORS,        None, 12, 0),
            (FlowFactors.TOKENS,        None, 12, 0),
            (FlowFactors.PITS,          None, 12, 2.0)
        ])
        result = predict_flow(student_id=11, task_id=12, practice_context=context)
        self.assertAlmostEquals(activation(1.9), result)


"""Unit test for skill update modul.
"""

from django.test import TestCase
from common.flow_factors import FlowFactors
from practice.models.practice_context import PracticeContext
import practice.services.parameters_update as parameters_update

class UpdateParametersTest(TestCase):

    def test_update_global_skill_function(self):
        skill = 0.25
        predicted_flow = 0
        reported_flow = -1
        expected = -0.47542871

        result = parameters_update.update_global_skill_function(
            skill, predicted_flow, reported_flow)

        self.assertAlmostEquals(result, expected)

    def test_update_other_skill_function(self):
        discrimination = 0

        for skill in range(-1, 2, 1):
            for reported_flow in range(-1, 2, 1):
                result = parameters_update.update_other_skill_function(
                    skill, reported_flow, discrimination)
                self.assertEquals(result, skill)

        discrimination = 1
        skill = -1
        for reported_flow in range(-1, 2, 1):
            result = parameters_update.update_other_skill_function(
                skill, reported_flow, discrimination)
            self.assertEquals(result, reported_flow)

        skill = 1
        for reported_flow in range(-1, 2, 1):
            result = parameters_update.update_other_skill_function(
                skill, reported_flow, discrimination)
            self.assertEquals(result, 1)

    def test_update_global_difficulty_function(self):
        difficulty = 0.25
        solution_count = 10
        predicted_flow = 0
        reported_flow = 1
        expected = 0.15

        result = parameters_update.update_global_difficulty_function(
            difficulty, solution_count, predicted_flow, reported_flow)

        self.assertAlmostEquals(result, expected)

    def test_update_parameters(self):
        context = PracticeContext([
            (FlowFactors.STUDENT_BIAS,  1, None, 0.20),
            (FlowFactors.CONDITIONS,    1, None, 0),
            (FlowFactors.LOOPS,         1, None, 0),
            (FlowFactors.LOGIC_EXPR,    1, None, -1),
            (FlowFactors.COLORS,        1, None, 0),
            (FlowFactors.TOKENS,        1, None, 1),
            (FlowFactors.PITS,          1, None, -1),
            (FlowFactors.TASK_BIAS,     None, 2, 3.7),
            (FlowFactors.CONDITIONS,    None, 2, 1),
            (FlowFactors.LOOPS,         None, 2, 0),
            (FlowFactors.LOGIC_EXPR,    None, 2, 0),
            (FlowFactors.COLORS,        None, 2, 1),
            (FlowFactors.TOKENS,        None, 2, 1),
            (FlowFactors.PITS,          None, 2, 0),
            ('solution-count',          None, 2, 10)
        ])

        expected_context = PracticeContext([
            (FlowFactors.STUDENT_BIAS,  1, None, 1.41517699),
            (FlowFactors.CONDITIONS,    1, None, 1),
            (FlowFactors.LOOPS,         1, None, 0),
            (FlowFactors.LOGIC_EXPR,    1, None, -1),
            (FlowFactors.COLORS,        1, None, 1),
            (FlowFactors.TOKENS,        1, None, 1),
            (FlowFactors.PITS,          1, None, -1),
            (FlowFactors.TASK_BIAS,     None, 2, 3.6),
            (FlowFactors.CONDITIONS,    None, 2, 1),
            (FlowFactors.LOOPS,         None, 2, 0),
            (FlowFactors.LOGIC_EXPR,    None, 2, 0),
            (FlowFactors.COLORS,        None, 2, 1),
            (FlowFactors.TOKENS,        None, 2, 1),
            (FlowFactors.PITS,          None, 2, 0),
            ('solution-count',          None, 2, 10)
        ])
        parameters_update.update_parameters(context, 1, 2, 1, 0)

        for key in context.get_skill_dict(1):
            self.assertAlmostEquals(
                context.get(key, 1, None), expected_context.get(key, 1, None))
        for key in context.get_difficulty_dict(2):
            self.assertAlmostEquals(
                context.get(key, None, 2), expected_context.get(key, None, 2))

    def test_update_parameters_with_same_predicted_and_reported_flow(self):
        # TODO: unhardcode flow-factors, sth. like
        #context = PracticeContext()
        #context.get = lambda parameter_name=None, task=None, student=None: 1

        context = PracticeContext([
            (FlowFactors.STUDENT_BIAS,  1, None, 0.0),
            (FlowFactors.CONDITIONS,    1, None, 0),
            (FlowFactors.LOOPS,         1, None, 0),
            (FlowFactors.LOGIC_EXPR,    1, None, -1),
            (FlowFactors.COLORS,        1, None, 0),
            (FlowFactors.TOKENS,        1, None, 1),
            (FlowFactors.PITS,          1, None, -1),
            (FlowFactors.TASK_BIAS,     None, 2, 3.7),
            (FlowFactors.CONDITIONS,    None, 2, 1),
            (FlowFactors.LOOPS,         None, 2, 0),
            (FlowFactors.LOGIC_EXPR,    None, 2, 0),
            (FlowFactors.COLORS,        None, 2, 1),
            (FlowFactors.TOKENS,        None, 2, 1),
            (FlowFactors.PITS,          None, 2, 0),
            ('solution-count',          None, 2, 10)
        ])

        expected_context = PracticeContext([
            (FlowFactors.STUDENT_BIAS,  1, None, 0.25),
            (FlowFactors.CONDITIONS,    1, None, 0),
            (FlowFactors.LOOPS,         1, None, 0),
            (FlowFactors.LOGIC_EXPR,    1, None, -1),
            (FlowFactors.COLORS,        1, None, 0),
            (FlowFactors.TOKENS,        1, None, 1),
            (FlowFactors.PITS,          1, None, -1),
            (FlowFactors.TASK_BIAS,     None, 2, 3.7),
            (FlowFactors.CONDITIONS,    None, 2, 1),
            (FlowFactors.LOOPS,         None, 2, 0),
            (FlowFactors.LOGIC_EXPR,    None, 2, 0),
            (FlowFactors.COLORS,        None, 2, 1),
            (FlowFactors.TOKENS,        None, 2, 1),
            (FlowFactors.PITS,          None, 2, 0),
            ('solution-count',          None, 2, 10)
        ])

        # action
        parameters_update.update_parameters(context, student_id=1, task_id=2,
                reported_flow=-1.0, predicted_flow=-1.0)

        # assert
        for key in context.get_skill_dict(student=1):
            self.assertAlmostEquals(
                context.get(key, student=1),
                expected_context.get(key, student=1))
        for key in context.get_difficulty_dict(task=2):
            self.assertAlmostEquals(
                context.get(key, task=2),
                expected_context.get(key, task=2))

    def test_update_parameters_without_reported_flow(self):
        context = PracticeContext([
            (FlowFactors.STUDENT_BIAS,  1, None, 0.0),
            (FlowFactors.CONDITIONS,    1, None, 0),
            (FlowFactors.LOOPS,         1, None, 0),
            (FlowFactors.LOGIC_EXPR,    1, None, -1),
            (FlowFactors.COLORS,        1, None, 0),
            (FlowFactors.TOKENS,        1, None, 1),
            (FlowFactors.PITS,          1, None, -1),
            (FlowFactors.TASK_BIAS,     None, 2, 3.7),
            (FlowFactors.CONDITIONS,    None, 2, 1),
            (FlowFactors.LOOPS,         None, 2, 0),
            (FlowFactors.LOGIC_EXPR,    None, 2, 0),
            (FlowFactors.COLORS,        None, 2, 1),
            (FlowFactors.TOKENS,        None, 2, 1),
            (FlowFactors.PITS,          None, 2, 0),
            ('solution-count',          None, 2, 10)
        ])

        expected_context = PracticeContext([
            (FlowFactors.STUDENT_BIAS,  1, None, 0.25),
            (FlowFactors.CONDITIONS,    1, None, 0),
            (FlowFactors.LOOPS,         1, None, 0),
            (FlowFactors.LOGIC_EXPR,    1, None, -1),
            (FlowFactors.COLORS,        1, None, 0),
            (FlowFactors.TOKENS,        1, None, 1),
            (FlowFactors.PITS,          1, None, -1),
            (FlowFactors.TASK_BIAS,     None, 2, 3.7),
            (FlowFactors.CONDITIONS,    None, 2, 1),
            (FlowFactors.LOOPS,         None, 2, 0),
            (FlowFactors.LOGIC_EXPR,    None, 2, 0),
            (FlowFactors.COLORS,        None, 2, 1),
            (FlowFactors.TOKENS,        None, 2, 1),
            (FlowFactors.PITS,          None, 2, 0),
            ('solution-count',          None, 2, 10)
        ])

        # action
        parameters_update.update_parameters(context, student_id=1, task_id=2,
                reported_flow=None, predicted_flow=1.2)

        # assert
        for key in context.get_skill_dict(student=1):
            self.assertAlmostEquals(
                context.get(key, student=1),
                expected_context.get(key, student=1))
        for key in context.get_difficulty_dict(task=2):
            self.assertAlmostEquals(
                context.get(key, task=2),
                expected_context.get(key, task=2))

"""Unit test for practice context module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import StudentModel
from common.flow_factors import FlowFactors
from decimal import Decimal
from datetime import datetime
from .practice_context import PracticeContext


class PracticeContextTest(TestCase):

    def test_set_get(self):
        context = PracticeContext()
        context.set('iq', value=5)
        context.set('iq', student=11, value=4)
        context.set('iq', task=12, value=6)
        context.set('iq', student=10, task=12, value=8)
        context.set('speed', student=11, value=9)
        self.assertEquals(5, context.get('iq'))
        self.assertEquals(4, context.get('iq', student=11))
        self.assertEquals(6, context.get('iq', task=12))
        self.assertEquals(8, context.get('iq', student=10, task=12))
        self.assertEquals(9, context.get('speed', student=11))

    def test_ininital_parameters(self):
        context = PracticeContext([
                ('iq', None, None, 5),
                ('iq', 11, None, 4),
                ('iq', None, 12, 6),
                ('iq', 10, 12, 8)
        ])
        self.assertEquals(5, context.get('iq'))
        self.assertEquals(4, context.get('iq', student=11))
        self.assertEquals(6, context.get('iq', task=12))
        self.assertEquals(8, context.get('iq', student=10, task=12))

    def test_update(self):
        context = PracticeContext([
                ('iq', None, None, 5),
                ('iq', 11, None, 4),
                ('iq', None, 12, 6),
                ('iq', 10, 12, 8)
        ])
        context.update('iq', update=lambda x: 10)
        context.update('iq', student=11, update=lambda x: x + 1)
        context.update('iq', task=12, update=lambda x: x * 2)
        context.update('iq', student=10, task=12, update=lambda x: x - 0.5)
        self.assertEquals(10, context.get('iq'))
        self.assertEquals(5, context.get('iq', student=11))
        self.assertEquals(12, context.get('iq', task=12))
        self.assertAlmostEquals(7.5, context.get('iq', student=10, task=12))

    def test_get_skill_dict(self):
        context = PracticeContext([
            (FlowFactors.STUDENT_BIAS, 11, None, 0.14),
            (FlowFactors.CONDITIONS, 11, None, 0),
            (FlowFactors.LOOPS, 11, None, 0.5),
            (FlowFactors.LOGIC_EXPR, 11, None, -0.5),
            (FlowFactors.COLORS, 11, None, 0),
            (FlowFactors.TOKENS, 11, None, 0),
            (FlowFactors.PITS, 11, None, 0)
        ])
        student_skill = context.get_skill_dict(student=11)
        self.assertAlmostEquals(0.14, student_skill[FlowFactors.STUDENT_BIAS])
        self.assertAlmostEquals(0, student_skill[FlowFactors.CONDITIONS])
        self.assertAlmostEquals(0.5, student_skill[FlowFactors.LOOPS])
        self.assertAlmostEquals(-0.5, student_skill[FlowFactors.LOGIC_EXPR])
        self.assertAlmostEquals(0, student_skill[FlowFactors.COLORS])
        self.assertAlmostEquals(0, student_skill[FlowFactors.TOKENS])
        self.assertAlmostEquals(0, student_skill[FlowFactors.PITS])

    def test_get_difficulty_dict(self):
        context = PracticeContext([
            (FlowFactors.TASK_BIAS, None, 12, 0.14),
            (FlowFactors.CONDITIONS, None, 12, 0),
            (FlowFactors.LOOPS, None, 12, 0.5),
            (FlowFactors.LOGIC_EXPR, None, 12, -0.5),
            (FlowFactors.COLORS, None, 12, 0),
            (FlowFactors.TOKENS, None, 12, 0),
            (FlowFactors.PITS, None, 12, 0)
        ])
        task_difficulty = context.get_difficulty_dict(task=12)
        self.assertAlmostEquals(0.14, task_difficulty[FlowFactors.TASK_BIAS])
        self.assertAlmostEquals(0, task_difficulty[FlowFactors.CONDITIONS])
        self.assertAlmostEquals(0.5, task_difficulty[FlowFactors.LOOPS])
        self.assertAlmostEquals(-0.5, task_difficulty[FlowFactors.LOGIC_EXPR])
        self.assertAlmostEquals(0, task_difficulty[FlowFactors.COLORS])
        self.assertAlmostEquals(0, task_difficulty[FlowFactors.TOKENS])
        self.assertAlmostEquals(0, task_difficulty[FlowFactors.PITS])

    def test_get_all_task_ids(self):
        context = PracticeContext([
                ('i', 10,   None, 1),
                ('i', None, 12, 1),
                ('i', 10,   12, 1)
        ])
        context.set('q', task=12, value=1)
        context.set('q', student=10, task=13, value=1)
        self.assertEquals({12, 13}, set(context.get_all_task_ids()))

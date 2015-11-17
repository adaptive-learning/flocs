"""Unit test of students skill model
"""

from django.test import TestCase
from .students_skill import StudentsSkillModel
from common.flow_factors import FlowFactors
from decimal import Decimal

class StudentsSkillModelTest(TestCase):

    def test_get_skill_dict(self):
        students_skills = StudentsSkillModel(
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

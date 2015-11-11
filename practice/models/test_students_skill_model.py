"""Unit test of students skill model
"""

from django.test import TestCase
from .students_skill import StudentsSkillModel
from decimal import Decimal

class StudentsSkillModelTest(TestCase):

    def test_to_vector(self):
        students_skills = StudentsSkillModel(
                programming=Decimal('0.14'),
                conditions=0,
                loops=0.5,
                logic_expr=-0.5,
                colors=0,
                tokens=0,
                pits=0,
                )
        student_vector = students_skills.to_vector()
        self.assertEquals(Decimal('0.14'), student_vector[0])
        self.assertEquals(Decimal('0'), student_vector[1])
        self.assertEquals(Decimal('0.5'), student_vector[2])
        self.assertEquals(Decimal('-0.5'), student_vector[3])
        self.assertEquals(Decimal('0'), student_vector[4])
        self.assertEquals(Decimal('0'), student_vector[5])
        self.assertEquals(Decimal('0'), student_vector[6])

"""Unit test of students skill manager
"""

from django.test import TestCase

from django.contrib.auth.models import User
from .students_skill import StudentsSkillModel
from .students_skill_manager import StudentsSkillManager

class StudentsSkillModelTest(TestCase):

    def test_get_created(self):
        u = User.objects.create()
        ss = StudentsSkillModel.objects.get_created(u)

        # assert default values
        self.assertEquals(StudentsSkillModel.INITIAL_STUDENT_BIAS, ss.programming)
        self.assertEquals(StudentsSkillModel.INITIAL_CONCEPT_SKILL, ss.conditions)
        self.assertEquals(StudentsSkillModel.INITIAL_CONCEPT_SKILL, ss.loops)
        self.assertEquals(StudentsSkillModel.INITIAL_CONCEPT_SKILL, ss.logic_expr)
        self.assertEquals(StudentsSkillModel.INITIAL_CONCEPT_SKILL, ss.colors)
        self.assertEquals(StudentsSkillModel.INITIAL_CONCEPT_SKILL, ss.tokens)
        self.assertEquals(StudentsSkillModel.INITIAL_CONCEPT_SKILL, ss.pits)

        ss2 = StudentsSkillModel.objects.get_created(u)

        # assert no other StudentSkill was created
        self.assertEquals(1, len(StudentsSkillModel.objects.all()))

        # assert it is the same Students Skills
        self.assertEquals(ss, ss2)



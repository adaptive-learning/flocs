"""
Unit test of instructions model.
"""

from django.test import TestCase
from .instructions_model import InstructionsModel
from common.flow_factors import FlowFactors

class TaskInstanceModelTest(TestCase):

    def test_create_instructions_instance(self):
        instructions = InstructionsModel(
            flow_factor=FlowFactors.PITS,
            text="some random text"
        )
        self.assertEquals(instructions.flow_factor, FlowFactors.PITS)
        self.assertEquals(instructions.text, "some random text")

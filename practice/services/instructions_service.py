"""
Service for obtaining correct instructions.
"""
import logging
from practice.models import StudentModel
from practice.models import TasksDifficultyModel
from practice.models import InstructionsModel
from common.flow_factors import FlowFactors

logger = logging.getLogger(__name__)

def get_instructions(student, task):
    """
    Returns list of instruction valid for the given student and task

    Args:
        student: student to whom the instructions are ment
        task: task which needs these instructions

    Returns:
        list of strings with instructions
    """
    skills = student.get_skill_dict()
    difficulties = \
            TasksDifficultyModel.objects.get(task=task).get_difficulty_dict()

    instructions = [InstructionsModel.objects.get(
        flow_factor=InstructionsModel.GENERAL_COMMENT).get_text()
    ]

    for factor in FlowFactors.game_factors() + FlowFactors.concept_factors():
        #logger.info("Factor: %s, skill: %s, difficulty: %s", factor,\
        #        skills[factor], difficulties[factor])
        if skills[factor] < 0 and difficulties[factor] > 0:
            instructions.append(InstructionsModel.objects.get(
                flow_factor=factor.value).get_text()
            )

    return instructions

"""
Service for obtaining correct instructions.
"""
import logging

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
    # NOTE: temporarily we are completelly ignoring instrustions (due to
    # massive refactoring)
    # TODO: implement getting instructions using Concepts
    instructions = []
    return instructions

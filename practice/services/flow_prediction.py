"""
Models for flow prediction

Flow factors given by a task:
    - global difficulty (task bias)
    - concept discriminations (conditions, loops, game concepts, ...)

Flow factors given by a user:
    - global problem solving skill (student bias)
    - concept skills
"""

from common.utils.activation import activation
from common.utils.math import dict_product
from common.flow_factors import FlowFactor

def predict_flow(student, task, practice_context):
    """
    Predict flow from information about student, task and practice context.
    Return real number with the following interpretation:
        ~ -1: too difficult task (leading to frustration)
        ~  0: optimaly difficul task (leading to flow)
        ~ +1: too easy task (leading to boredome)
    """
    student_flow_factors = student.get_skill_dict()
    task_flow_factors = task.get_difficulty_dict()
    student_flow_factors[FlowFactor.TASK_BIAS] = -1
    task_flow_factors[FlowFactor.STUDENT_BIAS] = 1

    # NOTE: We are ignoring practice context for now.

    potential = dict_product(student_flow_factors, task_flow_factors)
    flow = activation(potential)
    return flow


#def compute_task_context_flow_factors(student, task, practice_context):
#    """
#    Computes dictionary of factors affecting flow from both task and context.
#    """
#    context_flow_factors = practice_context.get_flow_factors()
#    flow_factors.update(context_flow_factors)
#    # TODO: add factors which depends also on the user (e.g. solution count)
#    return flow_factors

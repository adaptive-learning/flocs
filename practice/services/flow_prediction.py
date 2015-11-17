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
from common.flow_factors import FlowFactors

def predict_flow(student_id, task_id, practice_context):
    """
    Predict flow from information about student, task and practice context.
    Return real number with the following interpretation:
        ~ -1: too difficult task (leading to frustration)
        ~  0: optimaly difficul task (leading to flow)
        ~ +1: too easy task (leading to boredome)
    """
    student_flow_factors = practice_context.get_skill_dict(student_id)
    task_flow_factors = practice_context.get_difficulty_dict(task_id)
    student_flow_factors[FlowFactors.TASK_BIAS] = -1
    task_flow_factors[FlowFactors.STUDENT_BIAS] = 1
    potential = dict_product(student_flow_factors, task_flow_factors)
    flow = activation(potential)
    return flow

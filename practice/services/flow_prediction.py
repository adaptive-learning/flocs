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

def predict_flow(student, task, practice_context):
    """
    Predict flow from information about student, task and practice context.
    Return real number with the following interpretation:
        ~ -1: too difficult task (leading to frustration)
        ~  0: optimaly difficul task (leading to flow)
        ~ +1: too easy task (leading to boredome)
    """
    return 0.71  # temporary for testing
    # TODO: adjust the flow computation according to user/tasks model
    student_flow_factors = student.get_flow_factors()
    task_context_flow_factors = compute_task_context_flow_factors(student, task, practice_context)
    potential = dict_product(student_flow_factors, task_context_flow_factors)
    flow = activation(potential)
    return flow


def compute_task_context_flow_factors(student, task, practice_context):
    """
    Computes dictionary of factors affecting flow from both task and context.
    """
    flow_factors = task.get_flow_factors()
    context_flow_factors = practice_context.get_flow_factors()
    flow_factors.update(context_flow_factors)
    # TODO: add factors which depends also on the user (e.g. solution count)
    return flow_factors


def dict_product(dict1, dict2):
    """
    Computes dot product of vectors represented by dictionaries.
    """
    assert dict1.keys() == dict2.keys()

    product = 0.0
    for key in dict1:
        product += dict1[key] * dict2[key]
    return product

"""Updates skill of student and difficulty of task
"""
from math import exp
from common.flow_factors import FlowFactors

# Constants
# Speed of prediction learning for student bias
STUDENT_GLOBAL_SPEED = 1

# Speed of student learing for bias
STUDENT_GLOBAL_STEP = 1/4

# Steepness of exponential increase for bias
STUDENT_GLOBAL_STEEPNESS = 1/8

# Speed of task difficulty prediction learning
TASK_GLOBAL_SPEED = 1

def update_skill(student_id, task_id, reported_flow, predicted_flow,
                 practice_context):
    """Updates student's skill as well as task's difficulty base on predicted
    and real feedback from the student. Update is based on ELO.

    Args:
        student_id: id of student
        task_id: id of task the student finnished
        reported_flow: real flow collected from the student
        predicted_flow: flow predicted by our model for student and task
        practice_context: object with skill a difficulty vectors
    """
    update_student_skill(
        student_id,
        task_id,
        reported_flow,
        predicted_flow,
        practice_context
    )

    update_task_difficulty(
        task_id,
        reported_flow,
        predicted_flow,
        practice_context
    )

def update_student_skill(
        student_id, task_id, reported_flow, predicted_flow, practice_context):
    """ Updates student skill.

    Args:
        student_id: id of student
        task_id: id of task the student finnished
        reported_flow: real flow collected from the student
        predicted_flow: flow predicted by our model for student and task
        practice_context: object with skill a difficulty vectors
    """
    difficulty_dict = practice_context.get_difficulty_dict(task_id)

    for key in FlowFactors.game_factors() + FlowFactors.concept_factors():
        practice_context.update(
            key,
            student=student_id,
            task=None,
            update=lambda original: update_other_skill_function(
                original,
                reported_flow,
                difficulty_dict[key]
            )
        )

    practice_context.update(
        FlowFactors.STUDENT_BIAS,
        student=student_id,
        task=None,
        update=lambda original: update_global_skill_function(
            original,
            predicted_flow,
            reported_flow
        )
    )

def update_task_difficulty(
        task_id, reported_flow, predicted_flow, practice_context):
    """ Updates task difficulty.

    Args:
        task_id: id of task the student finnished
        reported_flow: real flow collected from the student
        predicted_flow: flow predicted by our model for student and task
        practice_context: object with skill a difficulty vectors
    """

    solution_count = practice_context.get_solution_count(task_id)

    practice_context.update(
        FlowFactors.TASK_BIAS,
        student=None,
        task=task_id,
        update=lambda original: update_global_difficulty_function(
            original,
            solution_count,
            predicted_flow,
            reported_flow
        )
    )


#def update_skill_function_full(
#        original, k_1, predicted_flow, reported_flow, a, k_2, k_3):
#    """ Function for computing new value of student skill.
#
#    Args:
#        original: original value of student skill
#        k_1: first constant
#        reported_flow: real flow collected from the student
#        predicted_flow: flow predicted by our model for student and task
#        a: concept discrimination
#        k_2: second constant
#        k_3: third constant
#    """
#
#    return original - k_1 * (predicted_flow - reported_flow) * a \
#            + k_2 * exp((-k_3) * original) * a

def update_global_skill_function(
        original, predicted_flow, reported_flow):
    """ Function for computing new value of student global skill.

    Args:
        original: original value of student skill
        k_1: first constant
        reported_flow: real flow collected from the student
        predicted_flow: flow predicted by our model for student and task
        a: concept discrimination
        k_2: second constant
        k_3: third constant
    """
    return original - STUDENT_GLOBAL_SPEED * (predicted_flow - reported_flow) \
            + STUDENT_GLOBAL_STEP * exp((-STUDENT_GLOBAL_STEEPNESS) * original)

def update_other_skill_function(original, reported_flow, discrimination):
    """ Function for computing new value of student game and programming skill.

    Args:
        original: original value of student skill
        reported_flow: real flow collected from the student
    """
    if discrimination != 1:
        return original
    else:
        return max(original, reported_flow)


def update_global_difficulty_function(
        original, solution_count, predicted_flow, reported_flow):
    """ Function for compution new value of task difficulty

    Args:
        original: original value of task difficulty
        k_4: first constant
        solution_count: number of successful solutions submitted
        reported_flow: real flow collected from the student
        predicted_flow: flow predicted by our model for student and task
    """
    return original + TASK_GLOBAL_SPEED/solution_count \
            * (predicted_flow - reported_flow)

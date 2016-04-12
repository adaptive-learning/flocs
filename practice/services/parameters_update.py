"""Updates skill of student and difficulty of task
"""
from math import exp
from common.flow_factors import FlowFactors

# Constants
# Speed of prediction learning for student bias
#STUDENT_GLOBAL_SPEED = 1
STUDENT_GLOBAL_SPEED = 0.35

# Speed of student learing for bias
#STUDENT_GLOBAL_STEP = 1/4
STUDENT_GLOBAL_STEP = 0.20

# Steepness of exponential increase for bias
STUDENT_GLOBAL_STEEPNESS = 0.1

# Speed of task difficulty prediction learning
TASK_GLOBAL_SPEED = 0.6

# Number we add to demoninator of normalizator of task difficulty update
SOLUTION_COUNT_START = 4

# Memory strength is individual, but for now we assume the same value for every
# student, 124 649 -> forget 50% after 1 day
MEMORY_STRENGTH = 124649

def update_parameters(practice_context, student_id, task_id, reported_flow,
        predicted_flow, last_solved_delta):
    """
    Updates student's skills as well as task's global difficulty base on
    difference beween predicted and real feedback collected from the student.
    Update is somewhat based on ELO.

    Args:
        practice_context: object with skill a difficulty parameters
        student_id: id of student
        task_id: id of task the student finnished
        reported_flow (float): real flow collected from the student
        predicted_flow (float): flow predicted by our model for student and task
    """
    update_student_skills(
        student_id,
        task_id,
        reported_flow,
        predicted_flow,
        last_solved_delta,
        practice_context
    )

    update_task_difficulty(
        task_id,
        reported_flow,
        predicted_flow,
        last_solved_delta,
        practice_context
    )

def update_student_skills(
        student_id, task_id, reported_flow, predicted_flow, last_solved_delta, practice_context):
    """ Updates all student's skills according to task he just solved.

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
            reported_flow,
            last_solved_delta
        )
    )

def update_task_difficulty(
        task_id, reported_flow, predicted_flow, last_solved_delta, practice_context):
    """ Updates task's global difficulty by calling the update function.

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
            reported_flow,
            last_solved_delta
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
        original, predicted_flow, reported_flow, last_solved_delta):
    """ A function for computing a new value of student's global skill. The
    difference of the two flows (times constant that corresponds to the "speed
    of learning") is subtracted from original skill. Than some small number is
    added as learning profit of solving the given task. The profit is in form
    of a exponetial function that is slighly linearized (according to the
    constants). These increments tend to fade out as the student already has
    high skill (the unlimited growth is practically imposible).

    Args:
        original: original value of student skill
        predicted_flow: flow predicted by our model for student and task
        reported_flow: real flow collected from the student
    """
    forgotten = forgetting(last_solved_delta)
    refined_skill_estimate = original - \
       STUDENT_GLOBAL_SPEED * flow_deviation(predicted_flow, reported_flow) * \
       forgotten

    # NOTE: the learning update is calculated using the already refined
    # before-task skill estimate
    learning_update = STUDENT_GLOBAL_STEP * \
         exp((-STUDENT_GLOBAL_STEEPNESS) * refined_skill_estimate) * forgotten
    updated_skill = refined_skill_estimate + learning_update
    return updated_skill

def update_other_skill_function(original, reported_flow, discrimination):
    """ A function for computing a new value of student's game and programming
    skills. This function never lowers the skill. The skill is raised if and
    only if the student reported the task to not be that difficult. Basically
    it returns the highes reported flow by the student in all of the tasks that
    tested this skill. Skills not tested by the task (discrimination is less
    that or equal to 0) always stays the same.

    Args:
        original: original value of student skill
        reported_flow: real flow collected from the student
        dicscrimination: how much the concept contributes to task difficulty
    """
    if reported_flow is not None and discrimination > 0.0:
        return max(original, reported_flow)
    else:
        return original

def update_global_difficulty_function(
        original, solution_count, predicted_flow, reported_flow, last_solved_delta):
    """ A function for computing a new value of the task global difficulty. It
    is very similar to update of student's global skill. The difference beween
    predicted and real flows is added to the original difficulty. The
    difference is normalized by the "speed of learning" and has smaller effects
    with growing number of collected solutions (the difficulty converges to
    some value).

    Args:
        original: original value of task difficulty
        solution_count: number of successful solutions submitted
        predicted_flow: flow predicted by our model for student and task
        reported_flow: real flow collected from the student
    """
    return original + TASK_GLOBAL_SPEED/(solution_count + SOLUTION_COUNT_START)\
            * flow_deviation(predicted_flow, reported_flow) \
            * forgetting(last_solved_delta)


def flow_deviation(predicted_flow, reported_flow):
    """
    Return deviation (surprise measure) between predicted and reported flow.
    The deviation can be negative, if predicted flow is lower then reported
    flow. If the reported_flow is None, the surprise is zero.
    """
    return predicted_flow - reported_flow if reported_flow is not None else 0.


def forgetting(time_delta):
    """
    Computes an amount of forgotten knowledge in the memory of the student about the task.
    Output 1 = student solves the task for the first time or fully forgotten the task.
    Output 0 = student fully remembers the task.

    Uses Ebbinghaus' forgetting curve:  e^(- t/S)
    where t = time, S = strength of the memory, for now same for every student.
    source: http://elearninginfographics.com/memory-retention-and-the-forgetting-curve-infographic/
    """
    if time_delta is None or time_delta < 0:
        return 1
    return 1 - exp(- time_delta / MEMORY_STRENGTH)

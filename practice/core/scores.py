""" Computing scores of tasks based on various criteria.
    All partial scores are between 0 and 1 (1 means best).
"""
import math
from common.utils.activation import AMPLITUDE
from practice.core.flow_prediction import predict_flow
from practice.core.efficiency import estimate_efficiency


class CombinedScoreComputer(object):
    def __init__(self, criteria, student, practice_context, combinator=sum):
        """
        Args:
            criteria - list of tuples (score function, weight)
            student - ID of student for whom to evaluate scores
            practice context
            combinator - function for combining partial scores
        """
        self.criteria = criteria
        self.combinator = combinator
        self.student = student
        self.practice_context = practice_context

    def combined_scores(self, tasks):
        return [(self.combined_score(task), task) for task in tasks]

    def combined_score(self, task):
        partial_scores = [score_fc(self.student, task, self.practice_context)
                          * weight
                          for score_fc, weight in self.criteria]
        score = self.combinator(partial_scores)
        return score


TIME_FOR_HALF_SCORE = 12 * 60 * 60  # 12 hours

def score_time_since_last_attempt(student, task, practice_context):
    """ Compute partial score for time since last attempt.
        The score is a real number between 0 (= the last attempt is recent)
        and 1 (= the last attempt was long time ago).
    """
    last_attempt_time = practice_context.get_last_attempt_time(student, task)
    time = practice_context.get_time()
    score = times_to_score(last_attempt_time, time)
    return score


def times_to_score(last_attempt_time, time):
    if last_attempt_time is None:
        return 1.
    seconds = (time - last_attempt_time).total_seconds()
    score = 1. - math.pow(0.5, seconds / TIME_FOR_HALF_SCORE)
    return score


def score_efficiency(student, task, practice_context):
    return estimate_efficiency(student, task, practice_context)


def score_flow(student, task, practice_context):
    flow = predict_flow(student, task, practice_context)
    score = flow_to_score(flow)
    return score


def flow_to_score(flow):
    """ Convert flow to a real number between 0 and 1.
    """
    score = 1. - ((flow / AMPLITUDE) ** 2)
    return score


def score_level(student, task, practice_context):
    student_level = practice_context.get('level', student=student)
    task_level = practice_context.get('level', task=task)
    score = levels_to_score(student_level, task_level)
    return score


def levels_to_score(student_level, task_level):
    if task_level > student_level:
        return 0
    return task_level / student_level

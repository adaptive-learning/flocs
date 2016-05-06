"""
Models for task selection.
"""

from random import choice
from common.utils.random import weighted_choice
from common.utils.math import product
from practice.core.scores import CombinedScoreComputer
from practice.core.scores import score_efficiency, score_flow, score_level
from practice.core.scores import score_time_since_last_attempt


class TaskSelector(object):
    """ Base class for task selection.
    """
    def select(self, task_ids, student_id, practice_context):
        NotImplementedError("Abstract method 'select' not implemented.")


class IdSpecifidedTaskSelector(TaskSelector):

    def __init__(self, task_id):
        self.task_id = task_id

    def select(self, task_ids, student_id, practice_context):
        if self.task_id not in task_ids:
            raise LookupError('Task with ID %s is not available.' % self.task_id)
        return self.task_id


class RandomTaskSelector(TaskSelector):

    def select(self, task_ids, student_id, practice_context):
        """ Select a random task.
        """
        task_id = choice(task_ids)
        return task_id


class RandomizedScoreTaskSelector(TaskSelector):
    """ Select task at random, but with probability of being selected according
        to its score.
    """
    # NOTE: for the plain product combinator, the weights are irrelevant
    CRITERIA_WEIGHTS = [
        (score_time_since_last_attempt, 1),
        (score_efficiency, 1),
        (score_level, 1),
    ]

    def select(self, task_ids, student_id, practice_context):
        score_computer = CombinedScoreComputer(
                criteria=self.CRITERIA_WEIGHTS,
                combinator=product,
                practice_context=practice_context,
                student=student_id)
        scored_tasks = score_computer.combined_scores(task_ids)
        #print('Random choice from:', sorted(scored_tasks))
        selected_task_id = weighted_choice(scored_tasks)
        return selected_task_id


class BestScoreTaskSelector(TaskSelector):

    """ Select task which maximizes score which is based on:
        - flow prediction
        - task efficiency (expected skill gain for unit of time)
        - time from the last attempt to solve this task
    """

    CRITERIA_WEIGHTS = [
        (score_flow, 5),
        (score_time_since_last_attempt, 16),
        (score_efficiency, 1),
    ]


    def select(self, task_ids, student_id, practice_context):
        score_computer = CombinedScoreComputer(
                criteria=self.CRITERIA_WEIGHTS,
                combinator=product,
                practice_context=practice_context,
                student=student_id)
        scored_tasks = score_computer.combined_scores(task_ids)
        best_task_id = max(scored_tasks)[1]
        return best_task_id

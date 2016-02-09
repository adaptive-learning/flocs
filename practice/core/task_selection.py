"""
Models for task selection.
"""

from random import choice
from common.utils.activation import AMPLITUDE
from practice.core.flow_prediction import predict_flow
import math


class TaskSelector(object):
    """
    Base class for task selection.
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
        """
        Select a random task.
        """
        task_id = choice(task_ids)
        return task_id


class ScoreTaskSelector(TaskSelector):

    WEIGHT_FLOW = 5
    WEIGHT_TIME = 10

    # seconds from the last attempt to get half of the maximum penalization
    TIME_FOR_HALF_SCORE = 60 * 60  # 1 hour


    def select(self, task_ids, student_id, practice_context):
        """
        Select task which maximizes score which is based on flow prediction
        and time from the last attempt to solve this task.

        It may use additional criteria in future, e.g. task effetiveness or
        exploration gain (how much information a task brings to the system).

        Return:
            id of selected task
        """
        def score(task_id):
            flow = predict_flow(student_id, task_id, practice_context)
            flow_score = self._score_flow(flow)

            last_attempt_time = practice_context.get_last_attempt_time(
                    student=student_id, task=task_id)
            current_time = practice_context.get_time()
            time_score = self._score_time_since_last_attempt(
                    last_attempt_time, current_time)

            score = self.WEIGHT_FLOW * flow_score\
                    + self.WEIGHT_TIME * time_score
            return score

        scored_tasks = [(score(task_id), task_id) for task_id in task_ids]
        ## necessary to sort only according to the 0th column (scores) only
        ## (because TaskModel in unsortable)
        #best_task = max(scored_tasks, key=lambda st: st[0])[1]
        best_task_id = max(scored_tasks)[1]
        return best_task_id

    def _score_flow(self, flow):
        """
        Compute partial score for flow prediction.

        Return:
            score - real number between -1 and 0
        """
        score = (-1) * ((flow / AMPLITUDE) ** 2)
        return score


    def _score_time_since_last_attempt(self, last_attempt_time, time):
        """
        Compute partial score for time since last attempt.

        The score is a real number between -1 (the last attempt is recent) and 0
        (= the last attempt was long time ago).
        """
        if last_attempt_time is None:
            return 0.0
        #seconds = time - last_attempt_time
        seconds = (time - last_attempt_time).total_seconds()
        score = -1 * math.pow(0.5, seconds / self.TIME_FOR_HALF_SCORE)
        return score

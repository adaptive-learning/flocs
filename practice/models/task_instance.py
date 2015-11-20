from django.db import models
from django.contrib.auth.models import User
from common.utils import activation
from tasks.models import TaskModel
from datetime import datetime

class FlowRating(object):
    UNKNOWN = 0
    DIFFICULT = 1
    RIGHT = 2
    EASY = 3

class TaskInstanceModel(models.Model):
    """
    Representation of a task taken by a user.
    """

    # student who took the task
    student = models.ForeignKey(User)

    # task which was assigned to the user
    task = models.ForeignKey(TaskModel)

    # when the task was shown to the student
    time_start = models.DateTimeField(default=datetime.now)

    # number of seconds the student spent solving the task
    time_spent = models.IntegerField(default=0)

    # flag whether the user eventually solved the task
    solved = models.BooleanField(default=False)

    # self-report about subjective difficulty feeling
    REPORTED_FLOW_VALUES = (
        (FlowRating.UNKNOWN,   'unknown'),
        (FlowRating.DIFFICULT, 'too difficult'),
        (FlowRating.RIGHT,     'just right'),
        (FlowRating.EASY,      'too easy'),
    )
    reported_flow = models.SmallIntegerField(choices=REPORTED_FLOW_VALUES,
            default=FlowRating.UNKNOWN)

    # predicted flow value
    predicted_flow = models.FloatField()

    # how many attempts did the user take (attempt = running a program)
    attempt_count = models.IntegerField(
            default=0)

    def __str__(self):
        templ = 'student={student}, task={task}, start={start}, time={time}' +\
                ', solved={solved} reported_flow={reported_flow}' + \
                ', predicted_flow={predicted_flow}'
        return templ.format(
            student=self.student.pk,
            task=self.task.pk,
            start=self.time_start,
            time=self.time_spent,
            solved=self.solved,
            reported_flow=self.reported_flow,
            predicted_flow=self.predicted_flow
        )

    def get_reported_flow(self):
        """
        Return reported flow as a real number or None if no feedback was
        provided.
        """
        if self.reported_flow == FlowRating.DIFFICULT:
            return -activation.AMPLITUDE
        elif self.reported_flow == FlowRating.RIGHT:
            return 0
        elif self.reported_flow == FlowRating.EASY:
            return activation.AMPLITUDE
        else:
            return None

    def get_predicted_flow(self):
        """Return predicted flow as a real number
        """
        return self.predicted_flow

    def update_after_attempt(self, attempt_count, time, solved, reported_flow=None):
        """
        Update information about the task instnace after a new attempt

        Args:
            attempt_count: order of an attempt (counting from 1)
            time: total number of seconds the student has been already solving
                the task
            solved: True if the student has solved the task
            reported_flow: number with the interpetration given by
                FlowRating (see above) or None if no rating was included
        """
        if attempt_count <= self.attempt_count:
            # obsolete attempt, ignore
            return

        self.attempt_count = attempt_count
        self.time_spent = time
        self.solved = solved

        if reported_flow is not None:
            if reported_flow not in range(4):
                raise ValueError('Invalid flow report number %s' % reported_flow)
            self.reported_flow = reported_flow

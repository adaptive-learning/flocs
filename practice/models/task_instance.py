from django.db import models
from common.utils import activation
from tasks.models import TaskModel
from practice.models import StudentModel
from datetime import datetime

class FlowRating(object):
    UNKNOWN = 0
    VERY_DIFFICULT = 1
    DIFFICULT = 2
    RIGHT = 3
    EASY = 4

class TaskInstanceModel(models.Model):
    """
    Representation of a task taken by a student.
    """

    # student who took the task
    student = models.ForeignKey(StudentModel)

    # task which was assigned to the student
    task = models.ForeignKey(TaskModel)

    # when the task was shown to the student
    time_start = models.DateTimeField(default=datetime.now)

    # when the last attempt report was sent
    time_end = models.DateTimeField(null=True, default=None)

    # number of seconds the student spent solving the task
    time_spent = models.IntegerField(default=0)
    # NOTE: we probably want to do not calculate it as (time_end - time start),
    # because the task might not be shown to the student immediately after
    # sending, we might want to not to include between-attempts pauses etc.

    # flag whether the student eventually solved the task
    solved = models.BooleanField(default=False)

    # self-report about subjective difficulty feeling
    REPORTED_FLOW_VALUES = (
        (FlowRating.UNKNOWN,   'unknown'),
        (FlowRating.VERY_DIFFICULT, 'very difficult'),
        (FlowRating.DIFFICULT, 'difficult'),
        (FlowRating.RIGHT, 'just right'),
        (FlowRating.EASY, 'easy'),
    )
    reported_flow = models.SmallIntegerField(choices=REPORTED_FLOW_VALUES,
            default=FlowRating.UNKNOWN)

    # predicted flow value
    predicted_flow = models.FloatField(default=None, null=True)

    # how many attempts did the student take (attempt = running a program)
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
        if self.reported_flow == FlowRating.VERY_DIFFICULT:
            return -activation.AMPLITUDE
        elif self.reported_flow == FlowRating.DIFFICULT:
            return -1.0
        elif self.reported_flow == FlowRating.RIGHT:
            return 0
        elif self.reported_flow == FlowRating.EASY:
            return 1.0
        else:
            return None

    def get_predicted_flow(self):
        """Return predicted flow as a real number
        """
        return self.predicted_flow

    def update_after_attempt(self, attempt_count, time, solved):
        """
        Update information about the task instnace after a new attempt

        Args:
            attempt_count: order of an attempt (counting from 1)
            time: total number of seconds the student has been already solving
                the task
            solved: True if the student has solved the task
        """
        # Obsolete attempt, ignore. Note that we allow for equality of
        # attempts count, which means that we can add more information to
        # the already reported attempt later.
        if attempt_count < self.attempt_count:
            return

        # Ignore additional attempts after the first successful one.
        if self.solved and attempt_count != self.attempt_count:
            return

        self.time_end = datetime.now()
        self.attempt_count = attempt_count
        self.time_spent = time
        self.solved = solved

    def update_after_giveup(self, time_spent):
        self.time_end = datetime.now()
        self.time_spent = time_spent

    def set_reported_flow(self, reported_flow):
        """
        Args:
            reported_flow: number with the interpetration given by
                FlowRating (see above) or None if no flow was provided
        """
        if reported_flow is None:
            return
        if reported_flow not in range(5):
            raise ValueError('Invalid flow report number %s' % reported_flow)
        self.reported_flow = reported_flow

from collections import namedtuple
from datetime import datetime
from django.db import models
from blocks.models import Block
from common.utils import activation
from concepts.models import Instruction
from tasks.models import TaskModel
from practice.models import StudentModel

class FlowRating(object):
    UNKNOWN = 0
    VERY_DIFFICULT = 1
    DIFFICULT = 2
    RIGHT = 3
    EASY = 4

    @classmethod
    def from_key(cls, key):
        return getattr(cls, key)


class TaskInstanceModel(models.Model):
    """
    Representation of a task taken by a student.
    """
    export_class = namedtuple('TaskInstance',
            ['task_instance_id', 'student_id', 'task_id',
             'time_start', 'time_end', 'time_spent',
             'solved', 'given_up', 'attempts', 'reported_flow',
             'instructions_ids', 'session_order'])

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

    # flags whether the student eventually solved/given up the task
    solved = models.BooleanField(default=False)
    given_up = models.BooleanField(default=False)

    # self-report about subjective difficulty feeling
    REPORTED_FLOW_VALUES = (
        (FlowRating.UNKNOWN,   'UNKNOWN'),
        (FlowRating.VERY_DIFFICULT, 'VERY_DIFFICULT'),
        (FlowRating.DIFFICULT, 'DIFFICULT'),
        (FlowRating.RIGHT, 'RIGHT'),
        (FlowRating.EASY, 'EASY'),
    )
    reported_flow = models.SmallIntegerField(choices=REPORTED_FLOW_VALUES,
            default=FlowRating.UNKNOWN)

    predicted_flow = models.FloatField(default=None, null=True)
    attempt_count = models.IntegerField(
        default=0,
        help_text='how many attempts did the student take (attempt = running a program)')
    earned_credits = models.SmallIntegerField(default=0, null=True)
    speed_bonus = models.BooleanField(default=False)

    instructions = models.ManyToManyField(Instruction,
        help_text='instructions presented to the student')

    blocks = models.ManyToManyField(Block,
        help_text='all blocks in toolbox (but only those required by the task were available)')

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

    def to_export_tuple(self):
        export_tuple = self.export_class(
                task_instance_id=self.pk,
                student_id=self.student.pk,
                task_id=self.task.pk,
                time_start=self.time_start,
                time_end=self.time_end,
                time_spent=self.time_spent,
                solved=self.solved,
                given_up=self.given_up,
                reported_flow=self.get_reported_flow_key(),
                attempts=self.attempt_count,
                session_order=self.get_session_order(),
                instructions_ids=[instruction.pk for instruction in self.instructions.all()])
        return export_tuple

    def get_session_order(self):
        session_instance = self.sessiontaskinstance_set.first()
        if session_instance is None:
            return None
        return session_instance.order

    def get_reported_flow_key(self):
        return self.get_reported_flow_display()

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

    def is_completed(self):
        return self.solved or self.given_up

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
        self.given_up = True
        self.earned_credits = 0

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

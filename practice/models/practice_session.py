from django.db import models

from practice.models import TaskInstanceModel
from practice.models import StudentModel
from datetime import datetime


class PracticeSession(models.Model):
    """
    Representation of a practice session.
    The session keeps counter of tasks in the session.
    """

    # time for practice session expiration
    EXPIRATION = 12 * 60 * 60 # half a day

    # student, owner of the session
    student = models.ForeignKey(StudentModel, null=True)

    # counter of the session tasks
    task_counter = models.PositiveSmallIntegerField(default=1)

    # last task instance started in the session
    last_task = models.ForeignKey(TaskInstanceModel, null=True)

    # duration of the session in sec, valid only after session termination
    duration = models.PositiveIntegerField(default=0)

    # active (private field)
    _active = models.BooleanField(default=True)

    # active (public property)
    def _get_active(self):
        # deactivate session if it is older then EXPIRATION parameter
        # keep duration = 0 if expired
        session_instances = self.task_instances_set.order_by('order')
        if len(session_instances) > 0:
            delta = datetime.now() - session_instances[0].task_instance.time_start
            if delta.total_seconds() > self.EXPIRATION:
                self._active = False
                self.save()
        return self._active

    def _set_active(self, input):
        self._active = input

    active = property(_get_active, _set_active)

    def get_task_instances(self):
        """
        Return list of task instances in this session in order they were taken
        by the student.
        """
        session_instances = self.task_instances_set.order_by('order')
        task_instances = [si.task_instance for si in session_instances]
        return task_instances

    def __str__(self):
        templ = ('session_id={session_id}, task_counter={task_counter}, '
                 'last_task={last_task}, active={active}')
        return templ.format(
            session_id=self.pk,
            task_counter=self.task_counter,
            last_task=self.last_task.pk,
            active=self.active
        )

from django.db import models

from practice.models import TaskInstanceModel
from practice.models import StudentModel

class PracticeSession(models.Model):
    """
    Representation of a practice session.
    The session keeps counter of tasks in the session.
    """

    # student, owner of the session
    student = models.ForeignKey(StudentModel, null=True)

    # counter of the session tasks 
    task_counter = models.PositiveSmallIntegerField(default=1)

    # last task instance started in the session
    last_task = models.ForeignKey(TaskInstanceModel, null=True)

    # active
    active = models.BooleanField(default=True)


    def __str__(self):
        templ = ('session_id={session_id}, task_counter={task_counter}, '
                 'last_task={last_task}, active={active}')
        return templ.format(
            session_id=self.pk,
            task_counter=self.task_counter,
            last_task=self.last_task.pk,
            active=self.active
        )

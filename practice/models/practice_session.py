from django.db import models
from tasks.models import TaskModel

class PracticeSession(models.Model):
    """
    Representation of a practice session.
    The session keeps counter of tasks in the session.
    """

    # counter of the session tasks 
    task_counter = models.PositiveSmallIntegerField(default=1)

    # last task started in the session
    last_task = models.ForeignKey(TaskModel, null=True)


    def __str__(self):
        templ = ('session_id={session_id}, task_counter={task_counter}, '
                 'last_task={last_task}')
        return templ.format(
            session_id=self.pk,
            task_counter=self.task_counter,
            last_task=self.last_task.pk
        )

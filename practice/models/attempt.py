from collections import namedtuple
from datetime import datetime
from django.db import models
from practice.models import TaskInstanceModel


class Attempt(models.Model):
    """ Representation of a single attempt to solve a given task instance
    """
    export_class = namedtuple('Attempt',
        ['attempt_id', 'task_instance_id', 'order',
         'time', 'success', 'code']
    )

    task_instance = models.ForeignKey(TaskInstanceModel,
        help_text='task instance being solved'
    )
    time = models.DateTimeField(
        default=datetime.now,
        help_text='time when the attempt was logged'
    )
    success = models.BooleanField(
        default=False,
        help_text='whether the task was solved by this attempt or not'
    )
    order = models.IntegerField(
        default=0,
        help_text='order of the attempt within this task instance'
    )
    code = models.TextField(
        help_text="XML representation of student's code",
    )

    def to_export_tuple(self):
        export_tuple = self.export_class(
            attempt_id=self.pk,
            task_instance_id=self.task_instance.pk,
            time=self.time,
            success=self.success,
            order=self.order,
            code=self.code
        )
        return export_tuple

from django.db import models
from practice.models import TaskInstanceModel
from practice.models import PracticeSession

class SessionTaskInstance(models.Model):
    """
    Representation of a task taken by a student in a session
    """
    session = models.ForeignKey(PracticeSession, related_name='task_instances_set')
    order = models.PositiveSmallIntegerField()
    task_instance = models.ForeignKey(TaskInstanceModel)

    class Meta:
        unique_together = (("session", "order"),)

    def __str__(self):
        template = 'session={session}, order={order}, task_instance={task_instance}'
        rendered_template = template.format(
            session=self.session.pk,
            order=self.order,
            task_instance=self.task_instance.pk)
        return rendered_template

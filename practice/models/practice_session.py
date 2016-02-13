from django.db import models

class PracticeSession(models.Model):
    """
    Representation of a practice session.
    The session keeps counter of tasks in the session.
    """

    # counter of the session tasks 
    task_counter = models.PositiveSmallIntegerField(default=1)


    def __str__(self):
        templ = 'session_id={session_id}, task_counter={task_counter}'
        return templ.format(
            session_id=self.pk,
            task_counter=self.task_counter
        )

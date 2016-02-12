from django.db import models

class PracticeSession(models.Model):
    """
    Representation of a session.
    For now, the session keeps only the pk.
    """

    def __str__(self):
        templ = 'session_id={session_id}'
        return templ.format(
            session_id=self.session_id.pk,
        )

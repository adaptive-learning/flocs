"""
Model for instruction that is shown to user in case he deals with new (or not
yet mastered) concept.
"""
from django.db import models
from concepts.models import Concept


class Instruction(models.Model):
    """ Instruction for better understanding of a specific concept by
        a student. Each instruction belongs to certain concept.
    """

    concept = models.ForeignKey(Concept)

    text = models.TextField(
            help_text='Text of the instruction shown to the student.')

    def __str__(self):
        templ = 'concept={concept}, text={text}'
        return templ.format(concept=self.concept, text=self.text)



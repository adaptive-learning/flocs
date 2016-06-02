"""
Model for instruction that is shown to user in case he deals with new (or not
yet mastered) concept.
"""
from django.db import models
from concepts.models import Concept
from collections import namedtuple


class Instruction(models.Model):
    """ Instruction for better understanding of a specific concept by
        a student. Each instruction belongs to certain concept.
    """
    export_class = namedtuple('Instruction',
            ['instruction_id', 'concept_id', 'order', 'text'])

    concept = models.ForeignKey(Concept)

    text = models.TextField(
            help_text='Text of the instruction shown to the student.')

    order = models.SmallIntegerField(
            help_text='instructions with lower "order" will be shown first',
            default=0)

    class Meta:
        ordering = ['order']

    def to_export_tuple(self):
        export_tuple = self.export_class(
                instruction_id=self.pk,
                concept_id=self.concept.pk,
                order=self.order,
                text=self.text)
        return export_tuple

    def __str__(self):
        templ = 'concept={concept}, text={text}'
        return templ.format(concept=self.concept, text=self.text)

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from common.flow_factors import FlowFactors
from concepts.models import Concept
from blocks.models import Block, Toolbox


def _get_initial_toolbox():
    return Toolbox.objects.get_initial_toolbox()


class StudentModel(models.Model):
    """Model for a student

       The student model keeps track of the current practice session.
       For every concept there is number between -1 and 1 representing skill in
       certain concept.
    """
    user = models.OneToOneField(User, primary_key=True)

    _seen_concepts = models.ManyToManyField(Concept,
            help_text='concepts already presented to the student')

    total_credits = models.IntegerField(
            help_text="total number of credits earned",
            default=0)

    free_credits = models.IntegerField(
            help_text="number of free credits to spend",
            default=0)

    toolbox = models.ForeignKey(Toolbox,
            help_text="blocks available to the student",
            default=_get_initial_toolbox,
            null=True)

    def get_level(self):
        if not self.toolbox:
            return 1
        return self.toolbox.level

    def get_seen_concepts(self):
        return set(self._seen_concepts.all())

    def mark_concept_as_seen(self, concept):
        self._seen_concepts.add(concept)

    def earn_credits(self, credits):
        self.total_credits += credits
        self.free_credits += credits

    def spend_credits(self, credits):
        if self.free_credits < credits:
            raise ValueError("Student doesn't have enough credits to spend.")
        self.free_credits -= credits

    def get_available_blocks(self):
        if self.toolbox is None:
            return list(Block.objects.all())
        return self.toolbox.get_all_blocks()

    def __str__(self):
        return 'pk={pk}'.format(pk=self.pk)

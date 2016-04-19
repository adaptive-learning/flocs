from django.db import models
from blocks.models import Block


class ConceptManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Concept(models.Model):
    """ A feature of students and tasks which influence the solving process.
        Concepts of a student determine her skill.
        Concepts of a task determine its difficulty.
    """
    objects = ConceptManager()

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BlockConcept(Concept):
    """ Concept of a single command block.
        A student either know or doesn't know what the block does.
        A task either require the block for the solution or not.
    """
    block = models.ForeignKey(Block)

    def save(self):
        if not name:
            self.name = 'block-' + block.identifier
        super().save()

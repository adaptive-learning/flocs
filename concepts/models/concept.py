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
    subconcepts = models.ManyToManyField('self')

    def get_subconcepts(self):
        return self.subconcepts.all()

    def __str__(self):
        return self.name


class ProgrammingConcept(Concept):
    """ Concept of a certain programming skill, such as usage of commands,
        loops, conditions or functions.
    """
    pass


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


class GameConcept(Concept):
    """ Concept describing some aspect of problem setting (e.g. tokens).
        A student is either familiar with this aspect or is not.
        A task either contains this aspect or does not .
    """
    checker = models.TextField(
            default=None, null=True,
            help_text="name of a Task method which check if it contains this concept")

    def is_contained_in(self, task):
        if not self.checker:
            return False
        concept_presence_checker = getattr(task, self.checker)
        return concept_presence_checker()


class EnvironmentConcept(Concept):
    """ Concept describing some aspect of the system environment
        A student is either familiar with this aspect or is not.
        Currently, all tasks contain all environment aspects.
    """
    pass

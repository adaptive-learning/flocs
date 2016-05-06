from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from concepts.models import Concept, EnvironmentConcept, GameConcept, BlockConcept
from blocks.models import Block, Toolbox


class TaskModel(models.Model):
    """Model for a task (exercise)
    """
    title = models.TextField()
    maze_settings = models.TextField(
            verbose_name="Maze settings in JSON",
            default='{}')
    workspace_settings = models.TextField(
            verbose_name="Workspace settings in JSON",
            default='{}')

    _contained_concepts = models.ManyToManyField(Concept,
            help_text='concepts contained in the task')

    toolbox = models.ForeignKey(Toolbox,
            help_text="minimal toolbox requried to solve this task",
            null=True, default=None)

    #  constants describing semantic of a maze grid
    _COLORS_FIELDS = [3, 4, 5]
    _FREE_FIELDS = [0, 2, 3, 4, 5]
    _PIT_FIELD = 6

    def get_level(self):
        if not self.toolbox:
            return 1
        return self.toolbox.level

    def get_contained_concepts(self):
        return set(self._contained_concepts.all())

    def infer_concepts(self):
        """ It only adds concepts as we do not need to remove concepts.
        """
        for concept in EnvironmentConcept.objects.all():
            self._add_concept(concept)
        for concept in GameConcept.objects.all():
            if concept.is_contained_in(self):
                self._add_concept(concept)
        blocks = self.get_required_blocks()
        for concept in BlockConcept.objects.all():
            if concept.block in blocks:
                self._add_concept(concept)

    def _add_concept(self, concept):
        self._contained_concepts.add(concept)

    def get_required_blocks(self):
        if self.toolbox is None:
            return list(Block.objects.all())
        return self.toolbox.get_all_blocks()

    def contains_tokens(self):
        return bool(self.get_tokens())

    def get_tokens(self):
        """ Return list of tokens or None, if there are no tokens
        """
        maze_settings_dict = json.loads(self.maze_settings)
        tokens = maze_settings_dict.get('tokens', None)
        if tokens == []:
            return None
        return tokens

    def contains_block_limit(self):
        return self.get_blocks_limit() is not None

    def get_blocks_limit(self):
        """ Return blocks limit or None, if there is no limit on blocks
        """
        workspace_settings_dict = json.loads(self.workspace_settings)
        return workspace_settings_dict.get('blocksLimit', None)

    def contains_pits(self):
        """ Return True if the task contains pits
        """
        grid = self.get_grid()
        for row in grid:
            for field in row:
                if field == self._PIT_FIELD:
                    return True
        return False

    def contains_colors(self):
        """ Return True if the task contains colors
        """
        grid = self.get_grid()
        for row in grid:
            for field in row:
                if field in self._COLORS_FIELDS:
                    return True
        return False

    def get_grid(self):
        """ Return 2D list representation of the maze
        """
        maze_settings_dict = json.loads(self.maze_settings)
        return maze_settings_dict['grid']

    def __str__(self):
        return '[{pk}] {title}'.format(pk=self.pk, title=self.title)

    def to_json(self):
        """Return JSON (dictionary) representation of the task.
        """
        maze_settings_dict = json.loads(self.maze_settings)
        workspace_settings_dict = json.loads(self.workspace_settings)
        task_dict = {
            'task-id': self.pk,
            'title': self.title,
            'maze-settings': maze_settings_dict,
            'workspace-settings': workspace_settings_dict
        }
        return task_dict


@receiver(post_save, sender=TaskModel)
def task_saved(sender, instance, created, **kwargs):
    """ After a task is saved for the first time, infer its concepts from its
        settings.  Note that we use signals instead of overriding save(),
        because save() is not called on loading fixtures.
    """
    if created:
        instance.infer_concepts()

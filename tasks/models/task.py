import json
import re
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from concepts.models import Concept, EnvironmentConcept, GameConcept, BlockConcept
from blocks.models import Block, Toolbox


class TaskModel(models.Model):
    """Model for a task (exercise)
    """
    title = models.TextField()

    maze_settings = models.TextField(
            verbose_name="maze settings (in JSON)",
            default='{}')

    workspace_settings = models.TextField(
            verbose_name="workspace settings (in JSON)",
            default='{}')

    _blocks_limit = models.PositiveSmallIntegerField(
            help_text="Limit on number of blocks student can use, including start block",
            null=True, default=None)

    _contained_concepts = models.ManyToManyField(Concept,
            help_text='concepts contained in the task')

    solution = models.TextField(
            help_text="XML representation of a Blockly program",
            null=True, default=None)

    toolbox = models.ForeignKey(Toolbox,
            help_text="minimal toolbox required to solve this task",
            null=True, default=None)

    #  constants describing semantic of a maze grid
    _COLORS_FIELDS = [3, 4, 5]
    _FREE_FIELDS = [0, 2, 3, 4, 5]
    _PIT_FIELD = 6

    # from which level to use block limit
    _BLOCK_LIMIT_LEVEL = 3

    def get_level(self):
        toolbox = self.get_toolbox()
        return toolbox.level if toolbox else 1

    def get_contained_concepts(self):
        return set(self._contained_concepts.all())

    def get_required_blocks(self):
        return self.get_toolbox().get_all_blocks()

    def get_toolbox(self, complete_if_none=True):
        if not self.toolbox and complete_if_none:
            return Toolbox.objects.get_complete_toolbox()
        return self.toolbox

    def get_blocks_limit(self):
        """ Return blocks limit or None, if there is no limit on blocks
        """
        return self._blocks_limit

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

    def contains_blocks_limit(self):
        return self.get_blocks_limit() is not None

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

    def get_workspace_settings(self):
        workspace_dict = json.loads(self.workspace_settings)
        workspace_dict['blocksLimit'] = self.get_blocks_limit()
        return workspace_dict


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
            'workspace-settings': self.get_workspace_settings()
        }
        return task_dict

    def infer_attributes_from_setting_and_solution(self):
        """ Infer toolbox, block limit and concepts from task setting and
            solution. The order of inference is important: concepts
            inference requires block limit to be knowns, block limit inference
            requires level (i.e. toolbox to be known).
        """
        assert self.maze_settings is not None and self.solution is not None
        self._infer_toolbox()
        self._infer_blocks_limit()
        self._infer_concepts()

    def _infer_blocks_limit(self):
        """ It only overrides block limit if it's not already set to
            a non-null value, if the task level is not small and if there
            is a solution to infer the block limit from
        """
        if self._blocks_limit is not None:
            return  # don't override non-null blocks limits
        if not self.solution or self.get_level() < self._BLOCK_LIMIT_LEVEL:
            return
        blocks = self._get_blocks_identifiers_in_solution()
        self._blocks_limit = len(blocks)

    def _infer_concepts(self):
        """ It only adds concepts as we do not need to remove concepts.
        """
        for concept in EnvironmentConcept.objects.all():
            self._add_concept(concept)
        for concept in GameConcept.objects.all():
            if concept.is_contained_in(self):
                self._add_concept(concept)
        blocks_identifiers = self._get_blocks_identifiers_in_solution()
        if not blocks_identifiers:
            return  # no solution -> no block concepts
        for concept in BlockConcept.objects.all():
            if concept.block.identifier in blocks_identifiers:
                self._add_concept(concept)

    def _infer_toolbox(self):
        assert self.solution is not None
        blocks = self._get_blocks_in_solution()
        self.toolbox = Toolbox.objects.get_first_toolbox_containing(blocks)

    def _add_concept(self, concept):
        self._contained_concepts.add(concept)

    def _get_blocks_in_solution(self):
        blocks_identifiers = self._get_blocks_identifiers_in_solution()
        blocks = [Block.objects.get_by_natural_key(identifier)
                  for identifier in blocks_identifiers]
        return blocks

    def _get_blocks_identifiers_in_solution(self):
        """ Return list of blocks identifiers as they appear in the solution
            If the solution is not provided, return None
        """
        if not self.solution:
            return None
        blocks = re.findall(r'<block type="(.*?)"', self.solution)
        return blocks


@receiver(post_save, sender=TaskModel)
def task_saved(sender, instance, created, **kwargs):
    """ After a task is saved for the first time, infer its concepts from its
        settings.  Note that we use signals instead of overriding save(),
        because save() is not called on loading fixtures.
    """
    task = instance  # Django needs the argument to be called "instance"
    if created and task.maze_settings is not None and task.solution is not None:
        task.infer_attributes_from_setting_and_solution()
        task.save()

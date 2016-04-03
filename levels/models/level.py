from functools import total_ordering
from django.db import models
from blocks.models import BlockModel
from .level_manager import LevelManager


@total_ordering
class Level(models.Model):
    """Model for a skill/difficulty level of a student/task
    """
    objects = LevelManager()

    # NOTE: in the future, levels might have more components,
    # but currently it only has a "block level" component
    block_level = models.SmallIntegerField(
        help_text="defines blocks corresponing to this level",
        default=1)
    credits = models.SmallIntegerField(
        help_text="credits required to earn the level",
        default=0)

    def get_new_blocks(self):
        return list(BlockModel.objects.filter(level=self.block_level))

    def get_all_blocks(self):
        levels = list(range(1, self.block_level+1))
        return list(BlockModel.objects.filter(level__in=levels))

    def __str__(self):
        return '[{block_level}] {new_blocks}'.format(
            block_level=self.block_level,
            new_blocks=' + '.join([block.name for block in self.get_new_blocks()]))

    def __lt__(self, other):
        if hasattr(other, 'block_level'):
            return self.block_level < other.block_level
        return self.block_level < other

    def __eq__(self, other):
        if hasattr(other, 'block_level'):
            return self.block_level == other.block_level
        return self.block_level == other

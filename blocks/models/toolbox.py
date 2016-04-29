from django.db import models
from blocks.models import Block
from .toolbox_manager import ToolboxManager


class Toolbox(models.Model):
    """ Model for a collection of blocks with associated level and credit value
    """
    objects = ToolboxManager()

    level = models.SmallIntegerField(
        help_text='defines ordering of toolboxes (higher level = more advanced toolbox)',
        default=1)

    name = models.CharField(
        max_length=50,
        unique=True,
        help_text='unique name of this toolbox')

    blocks = models.ManyToManyField(Block,
        help_text='all blocks contained in this toolbox')

    credits = models.SmallIntegerField(
        help_text='price to upgrade from the previous toolbox level',
        default=0)

    class Meta:
        ordering = ['level']

    def natural_key(self):
        return (self.name,)

    def get_new_blocks(self):
        current_blocks = set(self.get_all_blocks())
        prev_toolbox = Toolbox.objects.get_prev(self)
        old_blocks = set(prev_toolbox.get_all_blocks()) if prev_toolbox else set()
        new_blocks = current_blocks - old_blocks
        return list(new_blocks)

    def get_all_blocks(self):
        return list(self.blocks.all())

    def __str__(self):
        return '[{level}] {name}'.format(
            level=self.level,
            name=self.name)

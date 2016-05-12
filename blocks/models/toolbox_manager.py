from django.db import models

class ToolboxManager(models.Manager):

    IMPLIED_BLOCKS_IDENTIFIERS = ['start', 'math_number']

    def get_initial_toolbox(self):
        # toolboxes are ordered by their level
        return self.first()

    def get_complete_toolbox(self):
        return self.last()

    def get_first_toolbox_containing(self, blocks):
        """ Return toolbox with lowest level which contains given blocks
        """
        # disregard blocks which appear in workspace implicitly
        blocks = {block for block in blocks
                  if block.identifier not in self.IMPLIED_BLOCKS_IDENTIFIERS}
        for toolbox in self.all():
            if blocks.issubset(toolbox.get_all_blocks()):
                return toolbox
        raise ValueError('No toolbox containing all blocks.')

    def get_next(self, toolbox):
        """ Return the toolbox which follows the given toolbox.
            Return None, if there is no more adavanced toolbox available.
        """
        # toolboxes are ordered by their level
        return self.filter(level__gt=toolbox.level).first()

    def get_prev(self, toolbox):
        """ Return the toolbox which precedes the given toolbox.
            Return None, if there is no preceding toolbox.
        """
        return self.filter(level__lt=toolbox.level).last()

    def get_by_natural_key(self, name):
        return self.get(name=name)

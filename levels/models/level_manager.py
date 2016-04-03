from django.db import models

class LevelManager(models.Manager):

    fixtures = ['levels']

    def get_lowest_level(self):
        levels = list(self.all())
        if levels:
            return min(levels)
        return None

    def next_level(self, level):
        """
        Return the level which follows after the given level or None, if there
        is no next level.
        """
        try:
            next_block_level = level.block_level + 1
            return self.get(block_level=next_block_level)
        except self.model.DoesNotExist:
            return None


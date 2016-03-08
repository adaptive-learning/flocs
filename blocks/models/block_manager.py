from django.db import models

class BlockManager(models.Manager):

    def get_ordered_blocks(self):
        """Return all blocks in order defined by their difficulty
        """
        return self.order_by('difficulty')

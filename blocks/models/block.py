"""Definition of block model
"""

from django.db import models
import json

class BlockModel(models.Model):
    """Model for a block inside the Blockly environment
    """
    name = models.TextField(
        verbose_name="name of a block")

    identifiers = models.TextField(
        verbose_name="unique identifier(s) of a block(s) used internally")

    price = models.IntegerField(
        verbose_name="number of currency units required to buy this block",
        default=0)

    def __str__(self):
        return '[{pk}] {name}'.format(pk=self.pk, name=self.name)

    def to_json(self):
        """Returns JSON (dictionary) representation of the block.
        """
        block_dict = {
            'block-id': self.pk,
            'name': self.name,
            'identifiers': json.loads(self.identifiers),
            'price': self.price
        }
        return block_dict

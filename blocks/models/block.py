"""Definition of block model
"""

from django.db import models

class BlockModel(models.Model):
    """Model for a block inside the Blockly environment
    """
    name = models.TextField(
        verbose_name="name of a block")

    identifier = models.TextField(
        verbose_name="unique identifier of a block used internally")

    price = models.IntegerField(
        verbose_name="number of currency units required to buy this block")

    def __str__(self):
        return '[{pk}] {name}'.format(pk=self.pk, name=self.name)

    def to_json(self):
        """Returns JSON (dictionary) representation of the block.
        """
        block_dict = {
            'block-id': self.pk,
            'name': self.name,
            'identifier': self.identifier,
            'price': self.price
        }
        return block_dict

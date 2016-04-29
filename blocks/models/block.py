"""Definition of block model
"""

from django.db import models
import json
from .block_manager import BlockManager

class Block(models.Model):
    """Representation of a code block
    """
    objects = BlockManager()

    name = models.TextField(
        help_text="name of a block shown to students")

    identifier = models.CharField(
        max_length=50,
        unique=True,
        help_text="short unique identifier of the block")

    _expanded_identifiers = models.TextField(
        null=True,
        default=None,
        help_text="JSON array of identifiers for all variants of the block"
                  + "(null if there are no extra variants)")

    def natural_key(self):
        return (self.identifier,)

    def get_identifiers_list(self):
        if not self._expanded_identifiers:
            return [self.identifier]
        return json.loads(self._expanded_identifiers)

    def get_identifiers_condensed_list(self):
        return [self.identifier]

    def __str__(self):
        return '[{pk}] {name}'.format(pk=self.pk, name=self.name)

    def to_json(self):
        """Returns JSON (dictionary) representation of the block.
        """
        block_dict = {
            'block-id': self.pk,
            'name': self.name,
            'identifiers': self.get_identifiers_list(),
            'identifiers-condensed': self.get_identifiers_condensed_list()
        }
        return block_dict

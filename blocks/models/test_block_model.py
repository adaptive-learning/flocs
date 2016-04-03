"""Unit test of block model
"""

from django.test import TestCase
from .block import BlockModel

class BlockModelTest(TestCase):
    """Unit test case
    """

    def test_to_json(self):
        """Test of to_json method of block model class
        """
        name = 'foo'
        identifiers = '{"identifiers": ["bar"]}'
        identifiers_json = {'identifiers': ['bar']}
        identifiers_condensed = '{"identifiers_condensed": ["foo"]}'
        identifiers_condensed_json = {'identifiers_condensed': ['foo']}
        block = BlockModel(
            name=name,
            identifiers=identifiers,
            identifiers_condensed=identifiers_condensed)
        block_json = block.to_json()
        self.assertIn('name', block_json)
        self.assertIn('identifiers', block_json)
        self.assertEquals(block_json['name'], name)
        self.assertEquals(block_json['identifiers'], identifiers_json)
        self.assertEquals(block_json['identifiers-condensed'],
                          identifiers_condensed_json)

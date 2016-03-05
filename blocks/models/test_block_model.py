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
        identifier = 'bar'
        price = 12
        block = BlockModel(
            name=name,
            identifier=identifier,
            price=price)
        block_json = block.to_json()
        self.assertIn('name', block_json)
        self.assertIn('identifier', block_json)
        self.assertIn('price', block_json)
        self.assertEquals(block_json['name'], name)
        self.assertEquals(block_json['identifier'], identifier)
        self.assertEquals(block_json['price'], price)

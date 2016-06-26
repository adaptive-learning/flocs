""" Unit test of block model
"""

from django.test import TestCase
from .block import Block

class BlockTest(TestCase):
    def test_to_json(self):
        """ Test of to_json method of Block model
        """
        block = Block(name='Bar Bar', identifier='bar',
                      _expanded_identifiers='["bar1", "bar2"]')
        block_json = block.to_json()
        self.assertIn('name', block_json)
        self.assertIn('identifier', block_json)
        self.assertEquals(block_json['name'], 'Bar Bar')
        self.assertEquals(block_json['identifier'], 'bar')
        self.assertEquals(block_json['identifiers-expanded'], ['bar1', 'bar2'])

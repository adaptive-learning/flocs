from django.test import TestCase
from .block import Block

class BlockManagerTest(TestCase):

    fixtures = ['blocks']

    def test_all_ordered(self):
        ordered_blocks = Block.objects.all_ordered()
        self.assertEqual(Block.objects.count(), len(ordered_blocks))
        levels = [block.level for block in ordered_blocks]
        self.assertEqual(levels, sorted(levels))

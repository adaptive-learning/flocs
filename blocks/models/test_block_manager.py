from django.test import TestCase
from .block import BlockModel

class BlockManagerTest(TestCase):

    fixtures = ['blocks']

    def test_all_ordered(self):
        ordered_blocks = BlockModel.objects.all_ordered()
        self.assertEqual(BlockModel.objects.count(), len(ordered_blocks))
        levels = [block.level for block in ordered_blocks]
        self.assertEqual(levels, sorted(levels))

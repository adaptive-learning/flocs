from django.test import TestCase
from .block import BlockModel

class BlockManagerTest(TestCase):

    fixtures = ['blocks']

    def test_get_ordered_blocks(self):
        ordered_blocks = BlockModel.objects.get_ordered_blocks()
        difficulties = [block.difficulty for block in ordered_blocks]
        self.assertEqual(BlockModel.objects.count(), len(ordered_blocks))
        self.assertEqual(difficulties, sorted(difficulties))

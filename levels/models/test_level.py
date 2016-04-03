from django.test import TestCase
from .level import Level

class LevelTest(TestCase):

    def setUp(self):
        pass

    def test_comparision(self):
        self.assertTrue(Level(block_level=1) < Level(block_level=2))
        self.assertFalse(Level(block_level=2) < Level(block_level=1))
        self.assertTrue(Level(block_level=2) <= Level(block_level=2))
        self.assertTrue(Level(block_level=2) < 3)

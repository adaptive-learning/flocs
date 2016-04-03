from django.test import TestCase
from .level import Level

class LevelManagerTest(TestCase):

    fixtures = ['levels']

    def setUp(self):
        pass

    def test_get_lowest(self):
        self.assertEqual(Level.objects.get_lowest_level().block_level, 1)

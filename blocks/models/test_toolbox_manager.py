from django.test import TestCase
from .toolbox import Toolbox

class ToolboxManagerTest(TestCase):

    fixtures = ['blocks', 'toolboxes']

    def setUp(self):
        pass

    def test_get_initial_toolbox(self):
        self.assertEqual(Toolbox.objects.get_initial_toolbox().level, 1)


"""Unit test of task model
"""

from django.test import TestCase
from .task import TaskModel
from concepts.models import Concept


class TaskModelTest(TestCase):

    fixtures = ['blocks', 'toolboxes', 'concepts', 'tasks']

    def test_concepts_inference_task_54(self):
        task54 = TaskModel.objects.get(pk=54)
        inferred_concepts = task54.get_contained_concepts()
        expected_concepts = set([Concept.objects.get_by_natural_key(key)
                                 for key in ['ENV_MAZE', 'ENV_TOOLBOX',
                                             'ENV_WORKSPACE', 'ENV_SNAPPING',
                                             'ENV_RUN_RESET',
                                             'GAME_BLOCK_LIMIT', 'GAME_TOKENS',
                                             'BLOCK_MOVE', 'BLOCK_TURN',
                                             'BLOCK_REPEAT', 'BLOCK_WHILE',
                                             'BLOCK_CHECK_GOAL',
                                             'PROGRAMMING_SEQUENCE',
                                             'PROGRAMMING_REPEAT',
                                             'PROGRAMMING_WHILE',
                                             ]])
        self.assertSetEqual(inferred_concepts, expected_concepts)

    def test_concepts_inference_task_36(self):
        task36 = TaskModel.objects.get(pk=36)
        inferred_concepts = task36.get_contained_concepts()
        expected_concepts = set([Concept.objects.get_by_natural_key(key)
                                 for key in ['ENV_MAZE', 'ENV_TOOLBOX',
                                             'ENV_WORKSPACE', 'ENV_SNAPPING',
                                             'ENV_RUN_RESET',
                                             'GAME_BLOCK_LIMIT', 'GAME_COLORS',
                                             'BLOCK_MOVE', 'BLOCK_TURN',
                                             'BLOCK_WHILE', 'BLOCK_CHECK_GOAL',
                                             'BLOCK_CHECK_COLOR', 'BLOCK_CHECK_PATH',
                                             'BLOCK_IF', 'BLOCK_LOGIC',
                                             'PROGRAMMING_SEQUENCE',
                                             'PROGRAMMING_WHILE',
                                             'PROGRAMMING_IF',
                                             'PROGRAMMING_LOGIC',
                                             ]])
        self.assertSetEqual(inferred_concepts, expected_concepts)


    def test_concepts_inference_no_game_concepts(self):
        task = TaskModel.objects.get(pk=1)
        inferred_concepts = task.get_contained_concepts()
        expected_concepts = set([Concept.objects.get_by_natural_key(key)
                                 for key in ['ENV_MAZE', 'ENV_TOOLBOX',
                                             'ENV_WORKSPACE', 'ENV_SNAPPING',
                                             'ENV_RUN_RESET',
                                             'BLOCK_MOVE',
                                             'PROGRAMMING_SEQUENCE',
                                             ]])
        self.assertSetEqual(inferred_concepts, expected_concepts)

    def test_concepts_inference_colors(self):
        task = TaskModel.objects.get(pk=33)
        inferred_concepts = task.get_contained_concepts()
        colors_concept = Concept.objects.get_by_natural_key('GAME_COLORS')
        self.assertIn(colors_concept, inferred_concepts)

    def test_concepts_inference_pits(self):
        task = TaskModel.objects.get(pk=43)
        inferred_concepts = task.get_contained_concepts()
        pits_concept = Concept.objects.get_by_natural_key('GAME_PITS')
        self.assertIn(pits_concept, inferred_concepts)

    def test_blocks_limit_inference(self):
        self.assertEquals(TaskModel.objects.get(pk=1).get_blocks_limit(), None)
        self.assertEquals(TaskModel.objects.get(pk=11).get_blocks_limit(), 7)

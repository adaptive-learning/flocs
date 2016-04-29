"""Unit test of task model
"""

from django.test import TestCase
from .task import TaskModel
from concepts.models import Concept


class TaskModelTest(TestCase):

    fixtures = ['blocks', 'toolboxes', 'concepts', 'tasks']

    def test_concepts_inference(self):
        task54 = TaskModel.objects.get(pk=54)
        inferred_concepts = task54.get_contained_concepts()
        expected_concepts = set([Concept.objects.get_by_natural_key(key)
                                 for key in ['env-maze', 'env-toolbox',
                                             'env-workspace', 'env-snapping',
                                             'env-run-reset',
                                             'game-block-limit', 'game-tokens',
                                             'block-move', 'block-turn',
                                             'block-repeat', 'block-while',
                                             'block-check-goal']])
        self.assertSetEqual(inferred_concepts, expected_concepts)

    def test_concepts_inference_no_game_concepts(self):
        task = TaskModel.objects.get(pk=1)
        inferred_concepts = task.get_contained_concepts()
        expected_concepts = set([Concept.objects.get_by_natural_key(key)
                                 for key in ['env-maze', 'env-toolbox',
                                             'env-workspace', 'env-snapping',
                                             'env-run-reset',
                                             'block-move']])
        self.assertSetEqual(inferred_concepts, expected_concepts)

    def test_concepts_inference_colors(self):
        task = TaskModel.objects.get(pk=33)
        inferred_concepts = task.get_contained_concepts()
        colors_concept = Concept.objects.get_by_natural_key('game-colors')
        self.assertIn(colors_concept, inferred_concepts)

    def test_concepts_inference_pits(self):
        task = TaskModel.objects.get(pk=43)
        inferred_concepts = task.get_contained_concepts()
        pits_concept = Concept.objects.get_by_natural_key('game-pits')
        self.assertIn(pits_concept, inferred_concepts)

    def test_to_json(self):
        task = TaskModel(
                maze_settings='{"foo1": "bar1"}',
                workspace_settings='{"foo2": "bar2"}')
        task_json = task.to_json()
        self.assertIn('maze-settings', task_json)
        self.assertIn('workspace-settings', task_json)
        self.assertEquals(task_json['maze-settings'], {'foo1': 'bar1'})
        self.assertEquals(task_json['workspace-settings'], {'foo2': 'bar2'})

from django.test import TestCase
from unittest import skipIf
from tasks.models import TaskModel
from .initial_difficulties import TaskConcepts
from .initial_difficulties import InitialDifficultyEstimator


class InitialDifficultiesTest(TestCase):

    fixtures = ['blocks', 'toolboxes', 'tasks']

    def setUp(self):
        self.tasks_sorted_by_difficulty = [
            TaskModel.objects.get(pk=1),    # easiest task
            TaskModel.objects.get(pk=3),    # turning
            TaskModel.objects.get(pk=18),   # repeat
            TaskModel.objects.get(pk=20),   # repeat, more complex path
            TaskModel.objects.get(pk=37),   # while loop + goal/wall checks
            TaskModel.objects.get(pk=28),   # loops and conditions
            TaskModel.objects.get(pk=32),   # conditions, colors
            TaskModel.objects.get(pk=33),   # conditions, colors, tokens
            TaskModel.objects.get(pk=36),   # logical expressions
        ]

    def test_task_concepts_inference(self):
        self.assertEqual(len(TaskConcepts(TaskModel.objects.get(pk=1))), 0)
        self.assertEqual(len(TaskConcepts(TaskModel.objects.get(pk=18))), 2)
        self.assertEqual(len(TaskConcepts(TaskModel.objects.get(pk=37))), 3)
        self.assertEqual(len(TaskConcepts(TaskModel.objects.get(pk=32))), 4)
        self.assertEqual(len(TaskConcepts(TaskModel.objects.get(pk=33))), 5)
        self.assertEqual(len(TaskConcepts(TaskModel.objects.get(pk=36))), 5)
        self.assertEqual(len(TaskConcepts(TaskModel.objects.get(pk=38))), 6)

    def test_generating_reasonable_difficulties(self):
        estimator = InitialDifficultyEstimator()
        tasks = self.tasks_sorted_by_difficulty
        difficulties = [estimator.estimate_difficulty(task) for task in tasks]
        self.assertTrue(-3 < difficulties[0] < -1)
        self.assertTrue(1 < difficulties[-1] < 3)
        self.assertEqual(difficulties, sorted(difficulties))

    @skipIf(True, 'prints overview table')
    def test_print_difficulty_intensity(self):
        print('||')
        print('='*15)
        print('Task Intensity')
        estimator = InitialDifficultyEstimator()
        for task in self.tasks_sorted_by_difficulty:
            intensity = estimator.compute_difficulty_intensity(task)
            print('{pk: <4} {intst:.2f}'.format(pk=task.pk, intst=intensity))
        print('='*15)

    @skipIf(True, 'prints overview table')
    def test_print_difficulties(self):
        print('||')
        print('='*15)
        print('Task Difficulty')
        estimator = InitialDifficultyEstimator()
        tasks = self.tasks_sorted_by_difficulty
        for task in self.tasks_sorted_by_difficulty:
            difficulty = estimator.estimate_difficulty(task)
            print('{pk: <4} {dif:.2f}'.format(pk=task.pk, dif=difficulty))
        print('='*15)

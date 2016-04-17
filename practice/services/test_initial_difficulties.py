from django.test import TestCase
from unittest import skipIf
from tasks.models import TaskModel
from practice.models import TasksDifficultyModel
from .initial_difficulties import TaskConcepts
from .initial_difficulties import InitialDifficultyEstimator
from .initial_difficulties import TaskDifficultyCreator
from .initial_difficulties import generate


class InitialDifficultiesTest(TestCase):

    fixtures = ['levels', 'tasks']

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

    def test_create_task_difficulty(self):
        difficulty_creator = TaskDifficultyCreator()
        task = TaskModel.objects.get(pk=33)
        difficulty = difficulty_creator.create_task_difficulty(task)
        estimator = InitialDifficultyEstimator()
        self.assertEqual(difficulty.programming, estimator.estimate_difficulty(task))
        self.assertEqual(difficulty.loops, True)
        self.assertEqual(difficulty.conditions, True)
        self.assertEqual(difficulty.logic_expr, False)
        self.assertEqual(difficulty.colors, True)
        self.assertEqual(difficulty.tokens, True)
        self.assertEqual(difficulty.pits, False)

    def test_create_task_difficulty_no_concept(self):
        difficulty_creator = TaskDifficultyCreator()
        task = TaskModel.objects.get(pk=1)
        difficulty = difficulty_creator.create_task_difficulty(task)
        self.assertEqual(difficulty.loops, False)
        self.assertEqual(difficulty.conditions, False)
        self.assertEqual(difficulty.logic_expr, False)
        self.assertEqual(difficulty.colors, False)
        self.assertEqual(difficulty.tokens, False)
        self.assertEqual(difficulty.pits, False)


    def test_create_task_difficulty_most_concepts(self):
        difficulty_creator = TaskDifficultyCreator()
        task = TaskModel.objects.get(pk=43)
        difficulty = difficulty_creator.create_task_difficulty(task)
        self.assertEqual(difficulty.loops, True)
        self.assertEqual(difficulty.conditions, True)
        self.assertEqual(difficulty.logic_expr, True)
        self.assertEqual(difficulty.colors, False)
        self.assertEqual(difficulty.tokens, True)
        self.assertEqual(difficulty.pits, True)

    def test_generate(self):
        generate(update=False, create_fixture=False)
        task = TaskModel.objects.get(pk=33)
        difficulty = TasksDifficultyModel.objects.get(task=33)
        expected_difficulty = InitialDifficultyEstimator().estimate_difficulty(task)
        self.assertAlmostEqual(float(difficulty.programming), expected_difficulty, places=3)
        self.assertEqual(difficulty.loops, True)
        self.assertEqual(difficulty.conditions, True)
        self.assertEqual(difficulty.logic_expr, False)
        self.assertEqual(difficulty.colors, True)
        self.assertEqual(difficulty.tokens, True)
        self.assertEqual(difficulty.pits, False)

    def test_generate_updating(self):
        generated = generate(update=False, create_fixture=False)
        self.assertEqual(len(generated), TasksDifficultyModel.objects.count())
        self.assertEqual(len(generated), TaskModel.objects.count())
        TasksDifficultyModel.objects.first().delete()
        generated = generate(update=False, create_fixture=False)
        self.assertEqual(len(generated), 1)
        generated = generate(update=True, create_fixture=False)
        self.assertEqual(len(generated), TaskModel.objects.count())

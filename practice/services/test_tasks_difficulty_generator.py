"""Unit test of tasks difficulty generator
"""

from django.test import TestCase
from decimal import Decimal
from unittest import skipIf
from tasks.models import TaskModel
from levels.models import Level
from practice.models.tasks_difficulty import TasksDifficultyModel
from . import tasks_difficulty_generator


class TasksDifficultyGeneratorTest(TestCase):


    @skipIf(True, 'needs update')
    def test_generate(self):
        # create first task
        TaskModel.objects.create(pk=1,
                maze_settings=('{ '
                '"grid" : ['
                '    [0,0,6,1,1], '
                '    [0,0,0,0,0], '
                '    [4,1,0,1,0], '
                '    [1,1,1,1,0], '
                '    [2,4,0,1,0]], '
                '"tokens": [ [0,0], [1,1] ] }'
                ),
                workspace_settings=('{'
                '"blocksLimit" : 5'
                '}'),
                level=Level.objects.create(block_level=3))

        # create second task
        second_task = TaskModel.objects.create(pk=2,
                level=Level.objects.create(block_level=1))

        # create task difficulty to the second task
        TasksDifficultyModel.objects.create(
                task=second_task,
                programming=Decimal('0'),
                conditions=False,
                loops=False,
                logic_expr=False,
                colors=False,
                tokens=False,
                pits=False
                )

        # generate task difficulties
        tasks_difficulty_generator.generate()

        # test
        task_difs = TasksDifficultyModel.objects.filter(task__pk=1)
        self.assertEquals(1, len(task_difs))
        task_dif = list(task_difs)[0]
        self.assertEquals(False, task_dif.conditions)
        self.assertEquals(True, task_dif.loops)
        self.assertEquals(True, task_dif.logic_expr)
        self.assertEquals(False, task_dif.colors)
        self.assertEquals(True, task_dif.tokens)
        self.assertEquals(True, task_dif.pits)

    def test_number_of_blocks_category(self):
        blocks = ["loops_category", "foo_category", "bar_category"]
        num = tasks_difficulty_generator.number_of_blocks(blocks)
        self.assertEquals(3 * 5, num)

    def test_number_of_blocks(self):
        blocks = ["loops", "foo", "bar"]
        num = tasks_difficulty_generator.number_of_blocks(blocks)
        self.assertEquals(3, num)

    def test_reasonable_difficulty(self):
        # full model
        #TaskModel.objects.create(pk=1,
        #        maze_settings=('{ '
        #        '"grid" : ['
        #        '    [0,0,6,1,1], '
        #        '    [0,0,0,0,0] , '
        #        '    [4,1,0,1,0], '
        #        '    [1,1,1,1,0], '
        #        '    [2,4,0,1,0]], '
        #        '"tokens": [ [0,0], [1,1] ] }'
        #        ),
        #        workspace_settings=('{'
        #        '"blocksLimit" : 5,'
        #        '"toolbox": ['
        #        '    "foobar_category", '
        #        '    "loops_category", '
        #        '    "logic_ternary" ]'
        #        '}'))
        # model without categories
        TaskModel.objects.create(pk=2,
                maze_settings=('{ '
                '"grid" : ['
                '    [0,0,6,1,1], '
                '    [0,0,0,0,0] , '
                '    [4,1,0,1,0], '
                '    [1,1,1,1,0], '
                '    [2,4,0,1,0]], '
                '"tokens": [ [0,0], [1,1] ] }'
                ),
                workspace_settings=('{'
                '"blocksLimit" : 5,'
                '"toolbox": ['
                '    "foobar", '
                '    "loops", '
                '    "logic_ternary" ]'
                '}'))
        # model without categories and pits
        TaskModel.objects.create(pk=3,
                maze_settings=('{ '
                '"grid" : ['
                '    [0,0,0,1,1], '
                '    [0,0,0,0,0] , '
                '    [4,1,0,1,0], '
                '    [1,1,1,1,0], '
                '    [2,4,0,1,0]], '
                '"tokens": [ [0,0], [1,1] ] }'
                ),
                workspace_settings=('{'
                '"blocksLimit" : 5,'
                '"toolbox": ['
                '    "foobar", '
                '    "loops", '
                '    "logic_ternary" ]'
                '}'))
        # model without categories, pits and tokens
        TaskModel.objects.create(pk=4,
                maze_settings=('{ '
                '"grid" : ['
                '    [0,0,0,1,1], '
                '    [0,0,0,0,0] , '
                '    [4,1,0,1,0], '
                '    [1,1,1,1,0], '
                '    [2,4,0,1,0]] } '
                ),
                workspace_settings=('{'
                '"blocksLimit" : 5,'
                '"toolbox": ['
                '    "foobar", '
                '    "loops", '
                '    "logic_ternary" ]'
                '}'))
        # model without categories, pits, tokens and blocksLimit
        TaskModel.objects.create(pk=5,
                maze_settings=('{ '
                '"grid" : ['
                '    [0,0,0,1,1], '
                '    [0,0,0,0,0] , '
                '    [4,1,0,1,0], '
                '    [1,1,1,1,0], '
                '    [2,4,0,1,0]] }'
                ),
                workspace_settings=('{'
                '"toolbox": ['
                '    "foobar", '
                '    "loops", '
                '    "logic_ternary" ]'
                '}'))
        tasks_difficulty_generator.generate()
        tasks_difs = TasksDifficultyModel.objects.all()
        progr_difs = [tasks_dif.programming for tasks_dif in tasks_difs]
        prev = 5
        for dif in progr_difs:
            # check that previous task is harder than thisone
            self.assertTrue(dif < prev, msg="dif: " + str(dif) + " prev: " + str(prev))
            prev = dif





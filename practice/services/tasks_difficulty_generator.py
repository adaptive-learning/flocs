"""
    Tools for generating task's difficulty and guessing relation to concept
"""

from django.core import management
from decimal import Decimal
from math import tanh

from tasks.models.task import TaskModel
from practice.models.tasks_difficulty import TasksDifficultyModel

"""
    Specifies which blocks in some task implies game concept of the task.
"""
BLOCK_CONCEPT_MAPPING = {
        # conditions
        "maze_check_path"         : "conditions",
        "maze_check_path_left"    : "conditions",
        "maze_check_path_right"   : "conditions",
        "maze_check_path_front"   : "conditions",
        "controls_if"             : "conditions",
        "controls_if_else"        : "conditions",
        "controls_if_elseif_else" : "conditions",

        # loops
        "loops_category"   : "loops",
        "controls_repeat"  : "loops",
        "controls_while"   : "loops",
        "controls_for"     : "loops",
        "controls_forEach" : "loops",

        # logical expressions
        "boolean_category": "logic_expr",
        "logic_compared"  : "logic_expr",
        "logic_operation" : "logic_expr",
        "logic_negate"    : "logic_expr",
        "logic_boolean"   : "logic_expr",
        "logic_null"      : "logic_expr",
        "logic_ternary"   : "logic_expr",

        # colors
        "maze_check_color" : "colors"
        }

# average number of concepts
AVG_CONCEPTS = 5
# average number of blocks
AVG_BLOCKS = 5
# average number of tokens
AVG_TOKENS= 5

def generate():
    """
        Method generates data in tasks_difficulty model.

        For each task, it looks what are the block it uses and other properties
        and guess difficulty of the task and relation to concepts.

        If there is already model for some task, it will NOT update it.
    """
    # list of generated difficulties
    generated = []
    # take only those tasks, which do not have yet difficulty defined
    tasks = TaskModel.objects.filter(tasksdifficultymodel__pk__isnull=True)
    for task in tasks:
        json_task = task.to_json()
        maze = json_task['maze-settings']
        workspace = json_task['workspace-settings']
        # initialize array of concepts
        concepts = []

        # concepts: conditions, loops, logical expressions and colors
        blocks = workspace['toolbox']
        for block in blocks:
            if block in BLOCK_CONCEPT_MAPPING:
                concept = BLOCK_CONCEPT_MAPPING[block]
                concepts.append(concept)

        # concept: tokens
        if 'tokens' in maze:
            concepts.append('tokens')

        # concept: pits
        grid = maze['grid']
        for row in grid:
            for position in row:
                if position == 6:
                    concepts.append('pits')
                    break
            if 'pits' in concepts:
                break

        # concept: programming
        points = 0
        # number of concepts
        points += len(concepts) - AVG_CONCEPTS
        # number of blocks
        points += __number_of_blocks__(blocks) - AVG_BLOCKS
        # if there is blocks limit
        points += 5 * ('blocksLimit' in workspace) - 3
        # maze grid size
        points += len(maze['grid']) - 11
        # number of tokens
        if 'tokens' in workspace:
            points += len(workspace['tokens']) - AVG_TOKENS
        # loop concept
        points += 5 * ('loops' in concepts) - 3
        # logical expressions concepts
        points += 5 * ('logic_expr' in concepts) - 3
        # variables used
        points += 7 * ('variables_category' in blocks) - 4
        # functions used
        points += 7 * ('functions_category' in blocks) - 4
        # transfer to [-1,1]
        programming = tanh(points/50)

        # create task difficulty row in the db
        task_difficulty = TasksDifficultyModel.objects.create(
                task=task,
                programming=Decimal(programming),
                conditions=('conditions' in concepts),
                loops=( 'loops' in concepts),
                logic_expr=('logic_expr' in concepts),
                colors=('colors' in concepts),
                tokens=('tokens' in concepts),
                pits=('pits' in concepts)
                )
        #generated[task.pk] = [TasksDifficultyModel.objects.get(task=task).programming, concepts]
        generated.append(task_difficulty)

    # Store all task difficulties as fixture, necessary for isolated testing
    # and simulations
    create_task_difficulties_fixture()

    return generated

def create_task_difficulties_fixture():
    """
    Create fixture of all task difficultes
    """
    with open('practice/fixtures/task-difficulties.json', 'w') as f:
        management.call_command('dumpdata', 'practice.TasksDifficultyModel',
                indent=2, stdout=f)


def __number_of_blocks__(blocks):
    if blocks[0].endswith('category'):
        return 5*len(blocks)
    else:
        return len(blocks)


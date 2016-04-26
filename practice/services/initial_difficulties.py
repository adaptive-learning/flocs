from math import log, sqrt
import numpy as np
from tasks.models.task import TaskModel


class InitialDifficultyEstimator(object):
    """ Model for estimating initial difficulties using a simple heuristic
        Difficulties of all tasks are normalized so that they have mean 0 and
        standard deviation 1.
    """
    LEVEL_WEIGHT = 1.0
    GAME_CONCEPT_WEIGHT = 0.8
    MAZE_SIZE_WEIGHT = 1.2  # the logarithmic difference is already < 0.2
    FREE_SPACE_WEIGHT = 0.5

    def __init__(self):
        """ Precomputes mean and std of intensity of all tasks in DB
        """
        self._max_maze_size = 16
        all_tasks = TaskModel.objects.all()
        intensities = np.array([self.compute_difficulty_intensity(task)
                                for task in all_tasks])
        self._intensity_mean = np.mean(intensities)
        self._intensity_std = np.std(intensities)

    def estimate_difficulty(self, task):
        """ Returns difficulty for given task.
            Difficulty is normalized difficulty intensity (difficulties have
            mean 0 and standard deviation 1).
        """
        intensity = self.compute_difficulty_intensity(task)
        difficulty = (intensity - self._intensity_mean) / self._intensity_std
        return difficulty

    def compute_difficulty_intensity(self, task):
        """ Returns a real number which should be the higher the more difficult
            the task is. This number is unnormalized.

        Criteria (approx. in the order of importance):
            - level (currently captures available blocks) [1..10]
            - game concepts (not captured by the level): [0..4]
                - block limit, tokens, colors, pits
            - size of the maze (relative and on logarithmic scale [0..1]
            - relative amount of free space (paths) [0..1]
        """
        assert task.level is not None
        level = task.level.block_level
        game_concepts = self._number_of_game_concepts(task)
        fields = self._number_of_fields(task)
        maze_size = log(sqrt(fields)) / log(self._max_maze_size)
        free_space = self._number_of_free_fields(task) / fields
        intensity = ( self.LEVEL_WEIGHT * level
                    + self.GAME_CONCEPT_WEIGHT * game_concepts
                    + self.MAZE_SIZE_WEIGHT  * maze_size
                    + self.FREE_SPACE_WEIGHT * free_space)
        return intensity

    def _number_of_game_concepts(self, task):
        concepts = TaskConcepts(task)
        game_concepts = concepts & {'blocks-limit', 'colors', 'tokens', 'pits'}
        return len(game_concepts)

    def _number_of_fields(self, task):
        grid = task.get_grid()
        return len(grid) * len(grid[0])

    def _number_of_free_fields(self, task):
        grid = task.get_grid()
        free_fields = 0
        for row in grid:
            for field in row:
                free_fields += int(field in TaskModel._FREE_FIELDS)
        return free_fields


class TaskConcepts(set):
    CONCEPT_CHECKERS = {
        'loops':        lambda task: task.level >= 3,
        'conditions':   lambda task: task.level >= 7,
        'logic-expr':   lambda task: task.level >= 9,
        'blocks-limit': lambda task: task.get_blocks_limit() is not None,
        'colors':       lambda task: task.contains_colors(),
        'tokens':       lambda task: bool(task.get_tokens()),
        'pits':         lambda task: task.contains_pits()
    }
    def __init__(self, task):
        super().__init__()
        self.possible_keys = self.CONCEPT_CHECKERS.keys()
        for concept_name, has_concept in self.CONCEPT_CHECKERS.items():
            if has_concept(task):
                self.add(concept_name)

    def add(self, concept):
        if concept not in self.possible_keys:
            raise ValueError('<{0}> is not a valid concept.'.format(concept))
        super().add(concept)

    def __contains__(self, concept):
        if concept not in self.possible_keys:
            raise ValueError('<{0}> is not a valid concept.'.format(concept))
        return super().__contains__(concept)

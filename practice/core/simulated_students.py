from abc import ABCMeta, abstractmethod
from practice.models.task_instance import FlowRating
from common.flow_factors import FlowFactors


class SimulatedStudent(metaclass=ABCMeta):
    """ Base class for a simulated student
    """
    @abstractmethod
    def solve_task(self, task_difficulty):
        """ Simulate solving task.

        Return:
            - whether solved
            - number of seconds it took the student to solve the task
        """
        pass

    @abstractmethod
    def report_flow(self):
        """
        Return flow rating after a task (2=difficult, 3=right, 4=easy)
        """
        pass


class GeniusStudent(SimulatedStudent):
    """ Genius student solves any task in 1 sec and rate them as too easy
    """
    def solve_task(self, *args, **kwargs):
        return True, 1

    def report_flow(self, *args, **kwargs):
        return FlowRating.EASY


class SillyStudent(SimulatedStudent):
    """ Silly student solves any task in 1 hour and rate them as too difficult
    """
    def solve_task(self, *args, **kwargs):
        return True, 60 * 20

    def report_flow(self, *args, **kwargs):
        return FlowRating.DIFFICULT


class StupidStudent(SimulatedStudent):
    """ Stupid student solves only 1 from 5 tasks.
    """
    def __init__(self):
        self._counter = 0

    def solve_task(self, *args, **kwargs):
        solved = self._counter % 5 == 0
        self._counter += 1
        return solved, 60 * 20

    def report_flow(self, *args, **kwargs):
        return FlowRating.DIFFICULT


class FixedSkillStudent(SimulatedStudent):
    """ Student which does not learn
    """
    TRESHOLD_TOO_EASY = -1.0
    TRESHOLD_TOO_DIFFICULT = 0.8
    TRESHOLD_GIVE_UP = 1.2

    def __init__(self):
        self.difficulty = None

    def solve_task(self, task_difficulty):
        self.difficulty = task_difficulty[FlowFactors.TASK_BIAS]
        if self.difficulty < self.TRESHOLD_GIVE_UP:
            return True, 60 * 10
        else:
            return False, 60 * 10

    def report_flow(self, *args, **kwargs):
        if self.difficulty > self.TRESHOLD_TOO_DIFFICULT:
            return FlowRating.DIFFICULT
        elif self.difficulty < self.TRESHOLD_TOO_EASY:
            return FlowRating.EASY
        else:
            return FlowRating.RIGHT


class InteractiveStudent(SimulatedStudent):
    """ Allows for an interactive simulation
    """
    def solve_task(self, task_difficulty):
        #print('Task:', task_difficulty)
        time_input = input('Spent time (seconds): ')
        time = int(time_input)
        return True, time

    def report_flow(self):
        flow_input = input('Report flow (2=difficult, 3=right, 4=easy): ')
        flow = int(flow_input) if flow_input in '234' else 0
        return flow


SIMULATED_STUDENTS = {
    'genius': GeniusStudent,
    'silly': SillyStudent,
    'stupid': StupidStudent,
    'fixed-skill': FixedSkillStudent,
    'interactive': InteractiveStudent
}

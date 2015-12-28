from abc import ABCMeta, abstractmethod
from practice.models.task_instance import FlowRating


class SimulatedStudent(metaclass=ABCMeta):
    """
    Base class for a simulated student
    """
    @abstractmethod
    def spent_time(self, task_difficulty):
        """
        Return number of second it took the student to solve the task
        """
        pass

    @abstractmethod
    def report_flow(self, task_difficulty):
        """
        Return flow report after a task (1=difficult, 2=right, 3=easy)
        """
        pass


class GeniusStudent(SimulatedStudent):
    """
    Genius student solves any task in 10 seconds and all are too easy for her.
    """
    def spent_time(self, *args, **kwargs):
        return 10

    def report_flow(self, *args, **kwargs):
        return FlowRating.EASY


class StupidStudent(SimulatedStudent):
    """
    Stupid student solves any task in 30 minuts and all are too difficult for
    him.
    """
    def spent_time(self, *args, **kwargs):
        return 60 * 30

    def report_flow(self, *args, **kwargs):
        return FlowRating.DIFFICULT


class InteractiveStudent(SimulatedStudent):
    """
    Allows for interactive simulation
    """
    def spent_time(self, task_difficulty):
        #print('Task:', task_difficulty)
        time_input = input('Spent time (seconds): ')
        time = int(time_input)
        return time

    def report_flow(self, task_difficulty):
        flow_input = input('Report flow (1=difficult, 2=right, 3=easy): ')
        flow = int(flow_input) if flow_input in '123' else 0
        return flow


SIMULATED_STUDENTS = {
    'genius': GeniusStudent,
    'stupid': StupidStudent,
    'interactive': InteractiveStudent
}

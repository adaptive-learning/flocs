from django.contrib.auth.models import User
from abc import ABCMeta, abstractmethod
from math import inf
from common.simulation import Simulation
from tasks.models import TaskModel
from practice.models.task_instance import FlowRating
from practice.models import TasksDifficultyModel
from practice.services import practice_service

class SimulatedStudent(metaclass=ABCMeta):
    """
    Base class for a simulated user
    """
    @abstractmethod
    def spent_time(task_difficulty):
        """
        Return number of second it took the student to solve the task
        """
        pass

    @abstractmethod
    def report_flow(task_difficulty):
        """
        Return flow report after a task (1=difficult, 2=right, 3=easy)
        """
        pass


class GeniusStudent(SimulatedStudent):
    """
    Genius student solves any task in 10 seconds and all are too easy for her.
    """
    def spent_time(*args, **kwargs):
        return 10

    def report_flow(*args, **kwargs):
        return FlowRating.EASY


class StupidStudent(SimulatedStudent):
    """
    Stupid student solves any task in 30 minuts and all are too difficult for
    him.
    """
    def spent_time(*args, **kwargs):
        return 60 * 30

    def report_flow(*args, **kwargs):
        return FlowRating.DIFFICULT


class InteractiveStudent(SimulatedStudent):
    """
    Allows for interactive simulation
    """
    def spent_time(*args, **kwargs):
        time_input = input('Spent time (seconds): ')
        time = int(time_input)
        return time

    def report_flow(task_difficulty):
        #print('Task:', task_difficulty)
        flow_input = input('Report flow (1=difficult, 2=right, 3=easy): ')
        flow = int(flow_input) if flow_input in '123' else 0
        return flow


SIMULATED_STUDENTS = {
    'genius': GeniusStudent,
    'stupid': StupidStudent,
    'interactive': InteractiveStudent
}


class PracticeSimulation(Simulation):
    """
    Simulation of a practice session.
    """

    fixtures = ['tasks', 'instructions']

    def setUp(self):
        print('::setUp')

    def prepare(self, behavior, max_instances=20, max_time=inf):
        """
        Set simulatation parameters.

        Args:
            behavior: behavior of a simulated student (SimulatedStudent)
            max_task_instances: maximum length of session in number of instances
            max_time: maximum number of session in number of seconds
        """
        self.behavior = behavior
        self.max_instances = max_instances
        self.max_time = max_time

    def run_simulation(self):
        print('::run')
        print(self.behavior)
        print(len(TasksDifficultyModel.objects.all()))
        print(len(TaskModel.objects.all()))

        user = User.objects.create()

        instances_count, time_spent = 0, 0
        while instances_count < self.max_instances and time_spent < self.max_time:
            print('TODO: print info about student skill')
            task_dict = practice_service.get_next_task(user)
            print('TODO: output task ...')
            print('TODO: get task_difficulty')
            task_difficulty = None
            time = self.behavior.spent_time(task_difficulty)
            flow = self.behavior.report_flow(task_difficulty)
            report = {
                'task-instance-id': task_dict['task-instance-id'],
                'attempt': 0,
                'solved': True,
                'time': time,
                'flow-report': flow
            }
            process_attempt_report(user, report)
            instances_count += 1
            time_spent += time

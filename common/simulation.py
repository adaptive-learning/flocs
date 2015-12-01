from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from datetime import datetime
from django.test import TestCase
import csv
import json
import os

class SimulationLogger(object):

    def __init__(self, path_pattern):
        self.time = datetime.now()
        self.path_pattern = path_pattern
        self.rounds = []

    def new_round(self):
        self.rounds.append(OrderedDict())
        print('-' * 50)

    def log(self, key, value):
        assert(len(self.rounds) > 0, "Call new_round() before adding entries")
        self.rounds[-1][key] = value
        print('{key}: {value}'.format(key=key, value=value))

    def save(self, file_format):
        timestamp = self.time.strftime('%Y-%m-%d-%H-%M-%S')
        path = self.path_pattern.format(timestamp=timestamp) + '.' + file_format
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if file_format == 'json':
            self.save_json(path)
        elif file_format == 'csv':
            self.save_csv(path)
        else:
            raise ValueError('Unsupported file format: ' + file_format)

    def save_json(self, path):
        with open(path, 'w') as outfile:
            json.dump(self.rounds, outfile, indent=2, ensure_ascii=False)

    def save_csv(self, path):
        fieldnames = self.rounds[0].keys() if self.rounds else []
        with open(path, 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.rounds)


class Simulation(TestCase, metaclass=ABCMeta):
    """
    The simulation subclass Django's TestCase to enable complete isolation of
    the simulation. This is important for simulation to be reproducible,
    without isolation, each simulation would modify the database state
    and next simulation would be thus different.

    Usage:
    1. create a simulator instance (common.simulator.Simulator)
    2. create a simulation instance (common.simulation.Simulation)
    3. call simulator.run(simulation)
    """

    # simulation can specify database fixtures to load
    fixtures = None

    # simulation must specify a path where to store logs, the path should
    # include {timestamp} mark and should not include file extension, e.g.
    # 'practice/simulated-data/practice-simulation-{timestamp}
    log_path_pattern = None

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self)

        # _testMethodName is a name of a method to test by a test runner
        self._testMethodName = 'run_simulation'

        self.logger = SimulationLogger(path_pattern=self.log_path_pattern)
        self.prepare(*args, **kwargs)

    #def runTest(self):
    #    self.run_simulation()

    @abstractmethod
    def prepare(self, *args, **kwargs):
        """
        Set simulation parameters
        """
        pass

    @abstractmethod
    def run_simulation(self):
        """
        Run the simulation and build simulation log in self.simulation_log.
        This method is supposed to be run in isolation (i.e. with test
        database which will be destroyed after the simulation).
        """
        pass

    def get_simulation_log(self):
        if self.simulation_log is None:
            raise ValueError("Simulation log has not been created yet.")
        else:
            return self.simulation_log

from abc import ABCMeta, abstractmethod
from django.test import TestCase

class Simulation(TestCase):
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
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self)
        self.prepare(*args, **kwargs)

    def runTest(self):
        self.run_simulation()

    def prepare(self, *args, **kwargs):
        """
        Set simulation parameters
        """
        # TODO: make it an abstract method using ABC
        pass

    def run_simulation(self):
        """
        Run the simulaiton
        """
        # TODO: make it an abstract method using ABC
        pass

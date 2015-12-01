from django.test.runner import DiscoverRunner
from datetime import datetime

class Simulator(object):
    """
    Base class for running simulations in an isolated environment
    """
    def __init__(self):
        self._test_runner = _PassiveTestRunner()

    def run(self, simulation):
        self._test_runner.run_single_test(simulation)
        simulation.logger.save(file_format='csv')


class _PassiveTestRunner(DiscoverRunner):
    """
    Custom modification of test runner which does not perform test
    discovery
    """
    def run_single_test(self, test_instance):
        self.run_tests(test_labels=[], extra_tests=[test_instance])

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        """
        Build suite only from instantiated tests in 'extra_tests' list
        """
        suite = self.test_suite()
        for test in extra_tests:
            suite.addTest(test)
        return suite



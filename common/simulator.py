from django.test.runner import DiscoverRunner

class Simulator(object):
    """
    Base class for running simulations in an isolated environment
    """
    def __init__(self):
        #self.test_runner = CustomTestRunner(verbosity=0)
        self.test_runner = _PassiveTestRunner()

    def run(self, simulation):
        self.test_runner.run_tests(test_labels=[], extra_tests=[simulation])


class _PassiveTestRunner(DiscoverRunner):
    """
    Custom modification of test runner which does not perform test
    discovery
    """
    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        """
        Build suite only from instantiated tests in 'extra_tests' list
        """
        suite = self.test_suite()
        for test in extra_tests:
            suite.addTest(test)
        return suite



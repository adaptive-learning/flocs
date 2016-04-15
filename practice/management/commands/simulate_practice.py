from django.core.management.base import BaseCommand, CommandError
from math import inf
from common.simulator import Simulator
from practice.services.practice_simulation import PracticeSimulation
from practice.core.simulated_students import SIMULATED_STUDENTS
from analysis.plot_practice_session import show_practice_session_plot
from analysis.plot_practice_session import show_multiple_practice_session_plots


class Command(BaseCommand):
    help = 'Simulate practice session'

    def add_arguments(self, parser):
        parser.add_argument('--behavior',
                help='Student behavior. You can add another behaviors in practice/core/simulated_students.py.',
                choices=SIMULATED_STUDENTS.keys(),
                nargs='*',
                default=['interactive'])
        parser.add_argument('--max-instances',
                help='Limit on maximum number of task instances of the simulated session.',
                default=20,
                type=int)
        parser.add_argument('--max-time',
                help='Limit on maximum solving time of the simulated session.',
                default=inf,
                type=int)
        parser.add_argument('--plot',
                help="Show plot of the simulation after it's finished.",
                default=False,
                action='store_true')
        # TODO: add options for output (--quiet, --csv, --json, --plot)

    def handle(self, *args, **options):
        names = options['behavior']
        behaviors = [SIMULATED_STUDENTS[name]() for name in names]
        max_instances = options['max_instances']
        max_time = options['max_time']
        plot = options['plot']

        simulator = Simulator(save='csv')
        simulations = [PracticeSimulation(behavior=behavior,
                                          max_instances=max_instances,
                                          max_time=max_time)
                       for behavior in behaviors]
        logs = [simulator.run(simulation) for simulation in simulations]
        if plot:
            plot_logs(logs, names)


def plot_logs(logs, names):
    if len(logs) == 1:
        path = logs[0].get_path('csv')
        show_practice_session_plot(path)
    else:
        paths = [log.get_path('csv') for log in logs]
        show_multiple_practice_session_plots(paths, titles=names)

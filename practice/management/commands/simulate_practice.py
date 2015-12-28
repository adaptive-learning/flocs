from django.core.management.base import BaseCommand, CommandError
from math import inf
from common.simulator import Simulator
from practice.services.practice_simulation import PracticeSimulation
from practice.core.simulated_students import SIMULATED_STUDENTS


class Command(BaseCommand):
    help = 'Simulate practice session'

    def add_arguments(self, parser):
        parser.add_argument('--behavior',
                help='Student behavior. You can add another behaviors in practice/core/simulated_students.py.',
                choices=SIMULATED_STUDENTS.keys(),
                default='interactive')
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
        behavior = SIMULATED_STUDENTS[options['behavior']]()
        max_instances = options['max_instances']
        max_time = options['max_time']
        plot = options['plot']
        #print(student, max_instances, max_time)

        simulation = PracticeSimulation(
                behavior=behavior,
                max_instances=max_instances,
                max_time=max_time)
        simulator = Simulator(save='csv', plot=plot)
        simulator.run(simulation)

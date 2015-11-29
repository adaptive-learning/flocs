from django.core.management.base import BaseCommand, CommandError
from math import inf
from common.simulator import Simulator
from practice.services.practice_simulation import SIMULATED_STUDENTS
from practice.services.practice_simulation import PracticeSimulation

class Command(BaseCommand):
    help = 'Simulate practice session'

    def add_arguments(self, parser):
        parser.add_argument('--behavior',
                choices=SIMULATED_STUDENTS.keys(),
                default='interactive')
        parser.add_argument('--max-instances',
                default=20,
                type=int)
        parser.add_argument('--max-time',
                default=inf,
                type=int)

    def handle(self, *args, **options):
        behavior = SIMULATED_STUDENTS[options['behavior']]()
        max_instances = options['max_instances']
        max_time = options['max_time']
        #print(student, max_instances, max_time)

        simulation = PracticeSimulation(
                behavior=behavior,
                max_instances=max_instances,
                max_time=max_time)
        simulator = Simulator()
        simulator.run(simulation)

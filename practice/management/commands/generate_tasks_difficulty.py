from django.core.management.base import BaseCommand, CommandError

from practice.services import initial_difficulties


class Command(BaseCommand):
    help = ("Generate tasks difficulties according to the task's number of "
            "blocks, concepts etc. It generates only for the new tasks which "
            "have no difficulty specified - no overwriting.")

    def handle(self, *args, **options):
        generated = initial_difficulties.generate(update=False, create_fixture=True)
        self.stdout.write("Task difficulties generated: "
                + str(len(generated))
                + " [practice/fixtures/task-difficulties.json]")

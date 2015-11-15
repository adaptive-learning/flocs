from django.core.management.base import BaseCommand, CommandError

from practice.services import tasks_difficulty_generator


class Command(BaseCommand):
    help = ("Generate tasks difficulties according to the task's number of "
            "blocks, concepts etc. It generates only for the new tasks which "
            "have no difficulty specified - no overwriting.")

    def handle(self, *args, **options):
        generated = tasks_difficulty_generator.generate()
        if bool(generated):
            self.stdout.write("Tasks difficulty successfully generated: " + str(generated))
        else:
            self.stdout.write("No tasks difficulties were generated.")

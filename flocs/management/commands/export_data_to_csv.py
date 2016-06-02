from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from concepts.models import Concept, Instruction
import csv
import os


class Command(BaseCommand):
    help = "Export all data for analysis into CSV files."

    # all models to export need to define to_export_tuple() function
    models_to_export = [Concept, Instruction]

    def handle(self, *args, **options):
        self.export_all_tables()

    def export_all_tables(self):
        self.export_directory = settings.EXPORTED_DATA_DIR + '/tady-bude-datum/'
        os.makedirs(self.export_directory, exist_ok=True)
        self.stdout.write("Creating export of all data in {0}".format(self.export_directory))
        for model in self.models_to_export:
            self.export_model(model)

    def export_model(self, model):
        model_name = model.__name__
        self.stdout.write("- exporting model {0}".format(model_name))
        destination = self.export_directory +  model_name + '.csv'
        fieldnames = model.export_class._fields
        with open(destination, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for instance in model.objects.all():
                export_tuple = instance.to_export_tuple()
                writer.writerow(export_tuple)

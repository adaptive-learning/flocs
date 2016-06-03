from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from blocks.models import Block
from concepts.models import Concept, Instruction
from tasks.models import TaskModel
import csv
import os
import re


class Command(BaseCommand):
    help = "Export all data for analysis into CSV files."

    # all models to export need to define to_export_tuple() function
    models_to_export = [Block, Concept, Instruction, TaskModel]

    def handle(self, *args, **options):
        self.export_all_tables()

    def export_all_tables(self):
        datestamp = datetime.now().strftime('%Y-%m-%d')
        # the last empty path ('') is there to make it a directory, not a file
        self.export_directory = os.path.join(settings.EXPORTED_DATA_DIR,
                                             datestamp, '')
        os.makedirs(self.export_directory, exist_ok=True)
        self.stdout.write("Creating export of all data in {0}".format(self.export_directory))
        for model in self.models_to_export:
            self.export_model(model)

    def export_model(self, model):
        model_name = model.__name__
        file_name = model_name_to_file_name(model_name)
        self.stdout.write("- exporting model {0} to {1}".format(model_name, file_name))
        destination = os.path.join(self.export_directory, file_name)
        fieldnames = model.export_class._fields
        with open(destination, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(fieldnames)
            for instance in model.objects.all():
                export_tuple = instance.to_export_tuple()
                writer.writerow(export_tuple)

def model_name_to_file_name(name, extension='csv'):
    """ Convert name of a model (CamelCase) into a file name (hyphen-cases.csv)

    For example: Concept -> concepts.csv; HappyRabbit -> happy-rabbits.csv
    """
    name = name if name[-5:] != 'Model' else name[:-5]
    hyphened = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    file_name = hyphened.lower() + 's.' + extension
    return file_name

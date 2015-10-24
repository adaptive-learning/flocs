from django.db import models
from tasks.models import TaskModel
import json


class DifficultyModel(models.Model):
    """Model for a task (exercise)
    """
    difficulty = models.DecimalField(max_digits=4, decimal_places=3, verbose_name="Difficulty evaluation")
    task = models.OneToOneField(TaskModel, primary_key=True)

    def __str__(self):
        """Return string representation of the difficulty.
        """
        json_string = json.dumps(str(self.difficulty))
        return json_string

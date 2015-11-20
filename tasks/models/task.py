from django.db import models
import json


class TaskModel(models.Model):
    """Model for a task (exercise)
    """
    maze_settings = models.TextField(verbose_name="Maze settings in JSON")
    workspace_settings = models.TextField(verbose_name="Workspace settings in JSON")

    def __str__(self):
        """Return JSON string representation of the task.
        """
        json_string = json.dumps(self.to_json())
        return json_string

    def to_json(self):
        """Return JSON (dictionary) representation of the task.
        """
        maze_settings_dict = json.loads(self.maze_settings)
        workspace_settings_dict = json.loads(self.workspace_settings)
        task_dict = {
            'task-id': self.pk,
            'maze-settings': maze_settings_dict,
            'workspace-settings': workspace_settings_dict
        }
        return task_dict


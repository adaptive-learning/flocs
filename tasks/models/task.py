from django.db import models
import json
from levels.models import Level


class TaskModel(models.Model):
    """Model for a task (exercise)
    """
    title = models.TextField()
    maze_settings = models.TextField(
            verbose_name="Maze settings in JSON",
            default='{}')
    workspace_settings = models.TextField(
            verbose_name="Workspace settings in JSON",
            default='{}')

    level = models.ForeignKey(Level,
            help_text="minimum level required to attempt this task",
            null=True, default=None)

    def get_required_blocks(self):
        if self.level is None:
            return []
        return self.level.get_all_blocks()

    def __str__(self):
        return '[{pk}] {title}'.format(pk=self.pk, title=self.title)

    def to_json(self):
        """Return JSON (dictionary) representation of the task.
        """
        maze_settings_dict = json.loads(self.maze_settings)
        workspace_settings_dict = json.loads(self.workspace_settings)
        task_dict = {
            'task-id': self.pk,
            'title': self.title,
            'maze-settings': maze_settings_dict,
            'workspace-settings': workspace_settings_dict
        }
        return task_dict


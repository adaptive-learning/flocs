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

    #  constants describing semantic of a maze grid
    _COLORS_FIELDS = [3, 4, 5]
    _FREE_FIELDS = [0, 2, 3, 4, 5]
    _PIT_FIELD = 6

    def get_required_blocks(self):
        if self.level is None:
            return []
        return self.level.get_all_blocks()

    def get_grid(self):
        """ Return 2D list representation of the maze
        """
        maze_settings_dict = json.loads(self.maze_settings)
        return maze_settings_dict['grid']

    def get_tokens(self):
        """ Return list of tokens or None, if there are no tokens
        """
        maze_settings_dict = json.loads(self.maze_settings)
        tokens = maze_settings_dict.get('tokens', None)
        if tokens == []:
            return None
        return tokens

    def get_blocks_limit(self):
        """ Return blocks limit or None, if there is no limit on blocks
        """
        workspace_settings_dict = json.loads(self.workspace_settings)
        return workspace_settings_dict.get('blocksLimit', None)

    def contains_pits(self):
        """ Return True if the task contains pits
        """
        grid = self.get_grid()
        for row in grid:
            for field in row:
                if field == self._PIT_FIELD:
                    return True
        return False

    def contains_colors(self):
        """ Return True if the task contains colors
        """
        grid = self.get_grid()
        for row in grid:
            for field in row:
                if field in self._COLORS_FIELDS:
                    return True
        return False

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


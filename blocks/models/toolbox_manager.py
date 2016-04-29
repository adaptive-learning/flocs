from django.db import models

class ToolboxManager(models.Manager):


    def get_initial_toolbox(self):
        # toolboxes are ordered by their level
        return self.first()

    def get_next(self, toolbox):
        """ Return the toolbox which follows the given toolbox.
            Return None, if there is no more adavanced toolbox available.
        """
        # toolboxes are ordered by their level
        return self.filter(level__gt=toolbox.level).first()

    def get_prev(self, toolbox):
        """ Return the toolbox which precedes the given toolbox.
            Return None, if there is no preceding toolbox.
        """
        return self.filter(level__lt=toolbox.level).last()

    def get_by_natural_key(self, name):
        return self.get(name=name)

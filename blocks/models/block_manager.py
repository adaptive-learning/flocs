from django.db import models

class BlockManager(models.Manager):

    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)

from django.db import models
from tasks.models import TaskModel


class TasksDifficultyModel(models.Model):
    """Model for a task's difficulty
      
       For every concept there is a boolean value, where true means that 
       the task requires some knowledge of the specified concept.
       The first value is decimal number and represents general difficulty of
       the task.
    """
    
    # task to refer
    task = models.OneToOneField(TaskModel, primary_key=True)

    # programming concept difficulty
    programming = models.DecimalField(max_digits=4, decimal_places=3, verbose_name="General difficulty of the task")

    # conditions concept difficulty
    conditions = models.BooleanField(verbose_name="Difficulty of the conditions concept in the task")

    # loops concept difficulty
    loops = models.BooleanField(verbose_name="Difficulty of the loops concept in the task")

    # logic expressions concept difficulty
    logic_expr = models.BooleanField(verbose_name="Difficulty of the logic expressions concept in the task")

    # colors concept difficulty
    colors = models.BooleanField(verbose_name="Difficulty of the colors concept in the task")

    # tokens concept difficulty
    tokens = models.BooleanField(verbose_name="Difficulty of the tokens concept in the task")

    # pits concept difficulty
    pits = models.BooleanField(verbose_name="Difficulty of the pits concept in the task")

    def to_vector(self):
       """Return vector representation of the task difficulty.
          For each concept holds: 
           1 - the concept is related with the task
          -1 - the concept is not related with the task
       """
       return [self.programming,
               self.__convert_boolean_to_number__(self.conditions),
               self.__convert_boolean_to_number__(self.loops),
               self.__convert_boolean_to_number__(self.logic_expr),
               self.__convert_boolean_to_number__(self.colors),
               self.__convert_boolean_to_number__(self.tokens),
               self.__convert_boolean_to_number__(self.pits)
               ]

    def number_of_concepts(self):
        num = 0
        if self.conditions:
            num += 1
        if self.loops:
            num += 1
        if self.logic_expr:
            num += 1
        if self.colors:
            num += 1
        if self.tokens:
            num += 1
        if self.pits:
            num += 1
        return num

    def __convert_boolean_to_number__(self,boolean):
        if boolean:
            return 1
        else:
            return -1

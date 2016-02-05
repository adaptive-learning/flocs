from modeltranslation import translator
from .task import TaskModel

@translator.register(TaskModel)
class TaskTranslationOptions(translator.TranslationOptions):
    fields = ('title',)
    fallback_values = '[MISSING TITLE]'

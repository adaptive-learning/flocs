from modeltranslation import translator
from .instructions_model import InstructionsModel

@translator.register(InstructionsModel)
class InstructionsTranslationOptions(translator.TranslationOptions):
    fields = ('text',)
    fallback_values = '[MISSING TRANSLATION]'

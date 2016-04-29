from modeltranslation import translator
from .instruction import Instruction

@translator.register(Instruction)
class InstructionsTranslationOptions(translator.TranslationOptions):
    fields = ('text',)
    fallback_values = '[MISSING TRANSLATION]'

from modeltranslation import translator
from .block import Block

@translator.register(Block)
class BlockTranslationOptions(translator.TranslationOptions):
    fields = ('name',)
    fallback_values = {'name': '[MISSING NAME]'}

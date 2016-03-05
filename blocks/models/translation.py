from modeltranslation import translator
from .block import BlockModel

@translator.register(BlockModel)
class BlockTranslationOptions(translator.TranslationOptions):
    fields = ('name',)
    fallback_values = {'name': '[MISSING NAME]'}

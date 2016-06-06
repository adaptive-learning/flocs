from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models.block import Block
from .models.toolbox import Toolbox

class BlockAdmin(ImportExportModelAdmin):
    list_display = ('name', 'identifier', '_expanded_identifiers')
    search_fields = ('name',)
    ordering = ('name',)

class ToolboxAdmin(ImportExportModelAdmin):
    list_display = ('level', 'name', 'credits')
    search_fields = ('name',)
    ordering = ('level',)

admin.site.register(Block, BlockAdmin)
admin.site.register(Toolbox, ToolboxAdmin)

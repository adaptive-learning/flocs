from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Concept

class ConceptAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Concept, ConceptAdmin)

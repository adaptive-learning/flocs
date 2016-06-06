from django.contrib import admin
from .models.task import TaskModel
from import_export.admin import ImportExportModelAdmin
from practice.models import TaskInstanceModel

class TaskAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'title_en', 'toolbox', '_blocks_limit')
    search_fields = ('title','title_en')
    ordering = ('id',)


# Register your models here.
admin.site.register(TaskModel, TaskAdmin)

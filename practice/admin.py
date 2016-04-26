from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import StudentModel
from .models import TaskInstanceModel
from .models import StudentTaskInfoModel
from .models import PracticeSession
from .models import SessionTaskInstance


class StudentResource(resources.ModelResource):
    class Meta:
        model = StudentModel


class TaskInstanceResource(resources.ModelResource):
    class Meta:
        model = TaskInstanceModel


@admin.register(StudentModel)
class StudentsSkillAdmin(ImportExportModelAdmin):
    resource_class = StudentResource


@admin.register(TaskInstanceModel)
class TaskInstanceAdmin(ImportExportModelAdmin):
    resource_class = TaskInstanceResource


# other models registration
admin.site.register(StudentTaskInfoModel)
admin.site.register(PracticeSession)
admin.site.register(SessionTaskInstance)

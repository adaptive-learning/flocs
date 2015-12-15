from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import StudentsSkillModel
from .models import TasksDifficultyModel
from .models import TaskInstanceModel
from .models import StudentTaskInfoModel


class StudentsSkillResource(resources.ModelResource):
    class Meta:
        model = StudentsSkillModel


class TasksDifficultyResource(resources.ModelResource):
    class Meta:
        model = TasksDifficultyModel


class TaskInstanceResource(resources.ModelResource):
    class Meta:
        model = TaskInstanceModel


@admin.register(StudentsSkillModel)
class StudentsSkillAdmin(ImportExportModelAdmin):
    resource_class = StudentsSkillResource

@admin.register(TasksDifficultyModel)
class TasksDifficultyAdmin(ImportExportModelAdmin):
    resource_class = TasksDifficultyResource

@admin.register(TaskInstanceModel)
class TaskInstanceAdmin(ImportExportModelAdmin):
    resource_class = TaskInstanceResource


# other models registration
#admin.site.register(StudentsSkillModel)
#admin.site.register(TasksDifficultyModel)
#admin.site.register(TaskInstanceModel, TaskInstanceAdmin)
admin.site.register(StudentTaskInfoModel)

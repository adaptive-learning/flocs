from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import StudentModel
from .models import TaskInstanceModel
from .models import StudentTaskInfoModel
from .models import PracticeSession
from .models import SessionTaskInstance

# Amin classes
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('user', 'total_credits', 'free_credits', 'toolbox')
    search_fields = ('user__username',)
    ordering = ('user__username',)

class TaskInstanceAdmin(ImportExportModelAdmin):
    list_display = ('student', 'task', 'time_start', 'time_end', 'time_spent', 'solved', 'given_up')
    search_fields = ('student__user__username', 'task__title')
    ordering = ('student',)
    date_hierarchy = 'time_start'

class StudentTaskInfoAdmin(ImportExportModelAdmin):
    list_display = ('student', 'task', 'last_instance', 'last_solved_instance')
    search_fields = ('student', 'task')
    ordering = ('student',)

class SessionTaskInstanceAdmin(ImportExportModelAdmin):
    list_display = ('session', 'order', 'task_instance')
    ordering = ('session',)

class PracticeSessionAdmin(ImportExportModelAdmin):
    list_display = ('student', 'task_counter', 'last_task', '_active')
    ordering = ('student',)
    search_fields = ('student__user__username',)

# models registration
admin.site.register(StudentTaskInfoModel, StudentTaskInfoAdmin)
admin.site.register(PracticeSession, PracticeSessionAdmin)
admin.site.register(SessionTaskInstance, SessionTaskInstanceAdmin)
admin.site.register(StudentModel, StudentAdmin)
admin.site.register(TaskInstanceModel, TaskInstanceAdmin)

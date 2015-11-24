from django.contrib import admin
from .models import StudentsSkillModel
from .models import TasksDifficultyModel
from .models import TaskInstanceModel
from .models import StudentTaskInfoModel

# models registration
admin.site.register(StudentsSkillModel)
admin.site.register(TasksDifficultyModel)
admin.site.register(TaskInstanceModel)
admin.site.register(StudentTaskInfoModel)


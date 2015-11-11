from django.contrib import admin
from .models.students_skill import StudentsSkillModel
from .models.tasks_difficulty import TasksDifficultyModel

# models registration
admin.site.register(StudentsSkillModel)
admin.site.register(TasksDifficultyModel)


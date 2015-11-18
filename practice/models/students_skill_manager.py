from django.db import models

class StudentsSkillManager(models.Manager):
    def get_created(self, student):
        if self.model.objects.filter(student=student).exists():
            return self.model.objects.get(student=student)
        else:
            return self.model.objects.create(student=student)


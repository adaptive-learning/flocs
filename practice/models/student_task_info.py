from django.db import models
from tasks.models import TaskModel
from practice.models import StudentModel
from practice.models import TaskInstanceModel

class StudentTaskInfoModel(models.Model):
    """
    Persistent information about a student-task pair
    """

    student = models.ForeignKey(StudentModel)
    task = models.ForeignKey(TaskModel)

    class Meta:
        unique_together = ('student', 'task')
        index_together = ['student', 'task']

    # last instance of the task attempted by the student (not necessarily solved)
    last_instance = models.OneToOneField(TaskInstanceModel,
            related_name='+',  # = don't create backwards relation
            null=True,
            default=None)

    # last instance of the task solved by the student
    last_solved_instance = models.OneToOneField(TaskInstanceModel,
            related_name='+',  # = don't create backwards relation
            null=True,
            default=None)

    def is_solved(self):
        return self.last_solved_instance is not None

    def update(self, new_instance):
        self.last_instance = new_instance
        if new_instance.solved:
            self.last_solved_instance = new_instance

    def __str__(self):
        templ = 'student={student}, task={task}, last_instance={last_instance}'
        return templ.format(
            student=self.student.pk,
            task=self.task.pk,
            last_instance=self.last_instance.pk if self.last_instance else None
        )

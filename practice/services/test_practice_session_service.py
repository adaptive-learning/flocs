"""Unit test of practice session service
"""

from django.contrib.auth.models import User
from django.test import TestCase
from practice.models import StudentModel
from practice.models import PracticeSession
from practice.services import practice_session_service as service
from tasks.models import TaskModel

class PracticeSessionServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(user_id = self.user.id)

    def test_next_task_in_session(self):
        # assert student has no session assigned
        self.assertEquals(None, self.student.session)

        # create new task
        task = TaskModel.objects.create()
        task2 = TaskModel.objects.create()

        # start session
        service.next_task_in_session(self.student, task)

        # assert new session was created
        self.assertIsNotNone(self.student.session)
        sess = self.student.session
        self.assertEquals(1, sess.task_counter)
        self.assertEquals(task, sess.last_task)

        # proceed to next task
        service.next_task_in_session(self.student, task)
        # assert it wont change for the same task
        self.assertEquals(1, sess.task_counter)
        # proceed to next task
        service.next_task_in_session(self.student, task2)
        # assert change
        self.assertEquals(2, sess.task_counter)

        # set last task
        sess.task_counter = service.TASKS_IN_SESSION
        service.next_task_in_session(self.student, task)

        # assert new session was created
        self.student.session != sess
        self.assertEquals(1, self.student.session.task_counter)

    def test_end_session(self):
        # set up
        sess = PracticeSession.objects.create()
        self.student.session = sess

        # end session
        service.end_session(self.student)

        # assert it has really ended
        retrieved_student = StudentModel.objects.get(pk = self.student.pk)
        self.assertIsNone(retrieved_student.session)

"""Unit test of practice session service
"""

from django.contrib.auth.models import User
from django.test import TestCase
from practice.models import StudentModel
from practice.models import PracticeSession
from practice.services import practice_session_service as service

class PracticeSessionServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(user_id = self.user.id)

    def test_next_task_in_session(self):
        # assert student has no session assigned
        self.assertEquals(None, self.student.session)

        # start session
        service.next_task_in_session(self.student)

        # assert new session was created
        self.assertIsNotNone(self.student.session)
        sess = self.student.session
        self.assertEquals(1, sess.task_counter)

        # proceed to next task
        service.next_task_in_session(self.student)

        # assert again
        self.assertEquals(2, sess.task_counter)

        # set last task
        sess.task_counter = service.TASKS_IN_SESSION
        service.next_task_in_session(self.student)

        # assert new session was created
        self.student.session != sess
        self.assertEquals(1, self.student.session.task_counter)

    def test_get_task_in_session(self):
        # set up
        sess = PracticeSession.objects.create()
        sess.task_counter = 6
        self.student.session = sess

        # ask for task counter
        task_counter = service.get_task_in_session(self.student)

        # assert we picked the right session
        self.assertEquals(6, task_counter)

    def test_end_session(self):
        # set up
        sess = PracticeSession.objects.create()
        self.student.session = sess

        # end session
        service.end_session(self.student)

        # assert it has really ended
        retrieved_student = StudentModel.objects.get(pk = self.student.pk)
        self.assertIsNone(retrieved_student.session)

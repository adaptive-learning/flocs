"""Unit test of practice session service
"""

from django.contrib.auth.models import User
from django.test import TestCase
from practice.models import StudentModel
from practice.models import PracticeSession
from practice.models import TaskInstanceModel
from practice.models import SessionTaskInstance
from practice.services import practice_session_service as service
from tasks.models import TaskModel

from datetime import datetime, timedelta

class PracticeSessionServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(user=self.user)
        self.task = TaskModel.objects.create()
        self.taskInstance = TaskInstanceModel.objects.create(
                task=self.task,
                student=self.student)
        self.session = PracticeSession.objects.create(
                student=self.student,
                last_task=self.taskInstance)

    def test_next_task_in_session(self):
        self.assertEquals(1, self.session.task_counter)
        # create new task instance
        taskInstance = TaskInstanceModel.objects.create(
                task=self.task,
                student=self.student)
        # start session
        service.next_task_in_session(self.student, taskInstance)
        # assert counter was increased
        session = PracticeSession.objects.filter(student=self.student, _active=True)[0]
        self.assertEquals(2, session.task_counter)
        self.assertEquals(taskInstance, session.last_task)
        # set last task
        self.session.task_counter = service.TASKS_IN_SESSION
        self.session.save()
        service.next_task_in_session(self.student, taskInstance)
        # assert new session was created
        new_session = PracticeSession.objects.filter(
                student=self.student, _active=True)[0]
        self.assertNotEquals(self.session, new_session)
        self.assertEquals(1, new_session.task_counter)

    def test_has_unresolved_task(self):
        in_session = service.has_unresolved_task(self.student)
        self.assertTrue(in_session)
        # solve task and ask again
        self.taskInstance.solved = True
        self.taskInstance.save()
        in_session = service.has_unresolved_task(self.student)
        self.assertFalse(in_session)

    def test_get_active_task_instance(self):
        taskInstance = service.get_active_task_instance(self.session)
        self.assertEquals(self.taskInstance, taskInstance)
        # solve the task and ask again
        taskInstance.solved = True
        taskInstance.save()
        taskInstance = service.get_active_task_instance(self.session)
        self.assertIsNone(taskInstance)

    def test_get_session(self):
        session = service.get_session(self.student)
        self.assertEquals(self.session, session)

    def test_create_session(self):
        new_session = service.create_session(self.taskInstance)
        old_session = PracticeSession.objects.get(pk=self.session.pk)
        self.assertEquals(False, old_session.active)
        self.assertIsNotNone(new_session)
        self.assertNotEquals(old_session, new_session)
        self.assertEquals(1, new_session.task_counter)

    def test_end_session(self):
        # end session
        service.end_session(self.session)
        # get session
        new_session = PracticeSession.objects.filter(
                student=self.student, _active=True)
        # assert it has really ended
        self.assertEquals(0, len(new_session))

    def test_get_all_task_instances(self):
        instance1 = TaskInstanceModel.objects.create(task=self.task, student=self.student)
        instance2 = TaskInstanceModel.objects.create(task=self.task, student=self.student)
        instance3 = TaskInstanceModel.objects.create(task=self.task, student=self.student)
        session = service.create_session(instance3)
        service.next_task_in_session(self.student, instance1)
        task_instances = service.get_all_task_instances(session)
        self.assertEquals(len(task_instances), 2)
        self.assertEquals(task_instances[0].pk, instance3.pk)
        self.assertEquals(task_instances[1].pk, instance1.pk)

    def test_destroying_session_after_idle(self):
        SessionTaskInstance.objects.create(session=self.session, order=self.session.task_counter,
                task_instance=self.taskInstance)
        expiration = PracticeSession.EXPIRATION + 3600
        self.taskInstance.time_start = datetime.now() - timedelta(seconds=expiration)
        self.taskInstance.save()
        self.assertEquals(self.session.active, False)


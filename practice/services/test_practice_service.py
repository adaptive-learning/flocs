"""Unit test of task service
"""

from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from unittest import skipIf
from tasks.models import TaskModel
from practice.models import StudentModel
from practice.models import TaskInstanceModel
from practice.models import PracticeSession
from practice.models import SessionTaskInstance
from practice.models.task_instance import FlowRating
from concepts.models import Concept
from concepts.models import Instruction
from . import practice_service


class PracticeServiceWithFixturesTest(TestCase):

    fixtures = ['blocks', 'toolboxes', 'concepts', 'levels', 'tasks', 'instructions']

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(user=self.user)

    def test_process_attempt_report(self):
        instance = TaskInstanceModel.objects.create(task_id=1, student=self.student)
        report = {
            "task-instance-id": instance.pk,
            "task-id": 1,
            "attempt": 12,
            "solved": True,
            "time": 234,
        }
        practice_service.process_attempt_report(self.user, report)
        instance = TaskInstanceModel.objects.get(pk=instance.pk)
        self.assertEquals(12, instance.attempt_count)
        self.assertEquals(234, instance.time_spent)
        student = StudentModel.objects.get(user=self.user)
        self.assertGreater(student.total_credits, 0)

    def test_seen_concepts_marking(self):
        self.assertEqual(len(self.student.get_seen_concepts()), 0)
        instance = TaskInstanceModel.objects.create(task_id=1, student=self.student)
        practice_service.process_attempt_report(self.user, report={
            "task-instance-id": instance.pk,
            "task-id": 1,
            "attempt": 12,
            "solved": True,
            "time": 234})
        self.assertEqual(len(self.student.get_seen_concepts()), 6)

    def test_get_last_solved_delta(self):
        task = TaskModel.objects.get(pk=1)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=self.student,
                time_end=datetime(2016,4,6,18,26,7))
        delta = practice_service._get_last_solved_delta(self.student, task)
        self.assertIsNone(delta)
        TaskInstanceModel.objects.create(id=2, task_id=1, student=self.student,
                time_end=datetime(2016,4,8,10,20,0))
        delta = practice_service._get_last_solved_delta(self.student, task)
        self.assertEquals(143633, delta)

    def test_get_instructions(self):
        task = TaskModel.objects.get(pk=1)
        conc1 = Concept.objects.get_by_natural_key('block-move')
        conc2 = Concept.objects.get_by_natural_key('block-turn')
        task._contained_concepts = [conc1, conc2]
        task.save()
        self.student.mark_concept_as_seen(conc1)
        instructions = practice_service.get_instructions(task, self.student)
        expected = Instruction.objects.filter(concept=conc2)
        not_expected = Instruction.objects.filter(concept=conc1)
        for inst in expected:
            self.assertIn(inst, instructions)
        for inst in not_expected:
            self.assertNotIn(inst, instructions)


class PracticeServiceTest(TestCase):

    fixtures = ['blocks']

    def setUp(self):
        self.user = User.objects.create()

    def test_get_next_task_in_session(self):
        stored_task = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        task_info = practice_service.get_next_task_in_session(user=self.user)
        self.assertIsNotNone(task_info)
        self.assertEquals('{"foo": "bar"}', task_info.task.workspace_settings)
        self.assertEquals('{}', task_info.task.maze_settings)
        self.assertEquals(TaskInstanceModel.objects.first().id,
                task_info.task_instance.pk)
        student = StudentModel.objects.get(user=self.user)
        session = PracticeSession.objects.filter(student=student, _active=True)[0]
        self.assertEquals(session, task_info.session)
        task_instance = TaskInstanceModel.objects.get(student=student)
        self.assertEquals(session.last_task, task_instance)

    def test_no_task_available(self):
        # if there are no tasks available, task_service should raise
        # LookupError
        self.assertRaises(LookupError,
                practice_service.get_next_task_in_session, self.user)

    def test_get_task_by_id(self):
        stored_task = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        task_info = practice_service.get_task_by_id(user=self.user, task_id=stored_task.pk)
        self.assertIsNotNone(task_info)
        self.assertEquals('{"foo": "bar"}', task_info.task.workspace_settings)
        self.assertEquals('{}', task_info.task.maze_settings)
        self.assertEquals(TaskInstanceModel.objects.first().id,
                task_info.task_instance.pk)
        self.assertIsNone(task_info.session)

    def test_process_flow_report_solved_task(self):
        TaskModel.objects.create(id=1)
        student = StudentModel.objects.create(user=self.user)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=student)
        practice_service.process_flow_report(
                user=self.user,
                task_instance_id=1,
                reported_flow=FlowRating.EASY)
        task_instance = TaskInstanceModel.objects.get(id=1)
        self.assertEqual(task_instance.reported_flow, FlowRating.EASY)

    def test_process_giveup_report(self):
        TaskModel.objects.create(id=1)
        student = StudentModel.objects.create(user=self.user)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=student)
        practice_service.process_giveup_report(
                user=self.user,
                task_instance_id=1,
                time_spent=987)
        task_instance = TaskInstanceModel.objects.get(id=1)
        self.assertEqual(task_instance.reported_flow, FlowRating.VERY_DIFFICULT)
        self.assertEqual(task_instance.time_spent, 987)

    def test_get_session_overview(self):
        # set up
        student = StudentModel.objects.create(user=self.user)
        TaskModel.objects.create(id=1)
        task_instance = TaskInstanceModel.objects.create(id=1, task_id=1, student=student, time_end=datetime.now())
        session = PracticeSession.objects.create(id=1, student=student, last_task=task_instance)
        SessionTaskInstance.objects.create(session=session, task_instance=task_instance, order=1)

        # check
        sess_overview = practice_service.get_session_overview(self.user)
        task_instances = sess_overview.task_instances
        self.assertEquals(1, len(task_instances))
        self.assertEquals(task_instance, task_instances[0])
        overall_time = sess_overview.overall_time
        actual_time = task_instance.time_end - task_instance.time_start
        self.assertEquals(actual_time.seconds, overall_time)

    @skipIf(True, 'not implemented')
    def test_get_task_filtering(self):
        """ Tasks requiring blocks not in student's toolbox should be ignored
        """
        raise NotImplementedError

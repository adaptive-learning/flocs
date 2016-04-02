"""Unit test of task service
"""

from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from tasks.models import TaskModel
from blocks.models import BlockModel
from practice.models import StudentModel
from practice.models import TasksDifficultyModel
from practice.models import TaskInstanceModel
from practice.models import PracticeSession
from practice.models import SessionTaskInstance
from practice.models.task_instance import FlowRating
from practice.core.task_selection import ScoreTaskSelector
from . import practice_service


class PracticeServiceTest(TestCase):

    fixtures = ['instructions.json', 'blocks.xml']

    def setUp(self):
        self.user = User.objects.create()

    def test_get_next_task_in_session(self):
        stored_task = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        TasksDifficultyModel.objects.create(task=stored_task)
        task_info = practice_service.get_next_task_in_session(user=self.user)
        self.assertIsNotNone(task_info)
        self.assertEquals('{"foo": "bar"}', task_info.task.workspace_settings)
        self.assertEquals('{}', task_info.task.maze_settings)
        self.assertEquals(TaskInstanceModel.objects.first().id,
                task_info.task_instance.pk)
        student = StudentModel.objects.get(user=self.user)
        session = PracticeSession.objects.filter(student=student, active=True)[0]
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
        TasksDifficultyModel.objects.create(task=stored_task)
        task_info = practice_service.get_task_by_id(user=self.user, task_id=stored_task.pk)
        self.assertIsNotNone(task_info)
        self.assertEquals('{"foo": "bar"}', task_info.task.workspace_settings)
        self.assertEquals('{}', task_info.task.maze_settings)
        self.assertEquals(TaskInstanceModel.objects.first().id,
                task_info.task_instance.pk)
        self.assertIsNone(task_info.session)

    def test_process_attempt_report(self):
        student = StudentModel.objects.create(user=self.user)
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, solution_count=5)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=student,
                predicted_flow=0.22)
        report = {
            "task-instance-id": 1,
            "task-id": 1,
            "attempt": 12,
            "solved": True,
            "time": 234,
        }
        practice_service.process_attempt_report(self.user, report)
        difficulty = TasksDifficultyModel.objects.get(task_id=1)
        self.assertEquals(6, difficulty.solution_count)
        task_instance = TaskInstanceModel.objects.get(id=1)
        self.assertAlmostEquals(0.22, task_instance.predicted_flow)
        self.assertEquals(12, task_instance.attempt_count)
        self.assertEquals(234, task_instance.time_spent)
        student = StudentModel.objects.get(user=self.user)
        self.assertGreater(student.total_credits, 0)
        self.assertEqual(student.total_credits, student.free_credits)

    def test_process_flow_report_solved_task(self):
        difficulty_before_report = 1.0
        skill_before_report = -1.0
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, programming=difficulty_before_report)
        student = StudentModel.objects.create(user=self.user, programming=skill_before_report)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=student, predicted_flow=-1.0)
        practice_service.process_flow_report(
                user=self.user,
                task_instance_id=1,
                reported_flow=FlowRating.EASY)
        task_instance = TaskInstanceModel.objects.get(id=1)
        skill_after_report = StudentModel.objects.get(user_id=student.pk).programming
        difficulty_after_report = TasksDifficultyModel.objects.get(task_id=1).programming
        self.assertEqual(task_instance.reported_flow, FlowRating.EASY)
        self.assertGreater(skill_after_report, skill_before_report)
        self.assertLess(difficulty_after_report, difficulty_before_report)

    def test_process_giveup_report(self):
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, programming=-1.0)
        student = StudentModel.objects.create(user=self.user, programming=1.0)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=student, predicted_flow=1.0)
        skill_before_report = student.programming
        practice_service.process_giveup_report(
                user=self.user,
                task_instance_id=1,
                time_spent=987)
        task_instance = TaskInstanceModel.objects.get(id=1)
        self.assertEqual(task_instance.reported_flow, FlowRating.VERY_DIFFICULT)
        self.assertEqual(task_instance.time_spent, 987)
        skill_after_report = StudentModel.objects.get(user_id=student.pk).programming
        self.assertLess(skill_after_report, skill_before_report)

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

    def test_get_task_filtering(self):
        block1 = BlockModel.objects.get(pk=1)
        block2 = BlockModel.objects.get(pk=2)
        task1 = TaskModel.objects.create(block_level=1)
        task2 = TaskModel.objects.create(block_level=2)
        TasksDifficultyModel.objects.create(task=task1, programming=0.0)
        TasksDifficultyModel.objects.create(task=task2, programming=1.0)
        student = StudentModel.objects.create(user=self.user, programming=1.0)
        student.available_blocks = [block1]
        task_info = practice_service.get_task(student=student, task_selector=ScoreTaskSelector())
        self.assertEqual(task_info.task_instance.task.pk, task1.pk)

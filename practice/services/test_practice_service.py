"""Unit test of task service
"""

from django.contrib.auth.models import User
from django.test import TestCase
from tasks.models import TaskModel
from practice.models import StudentModel
from practice.models import TasksDifficultyModel
from practice.models import TaskInstanceModel
from practice.models import PracticeSession
from practice.models.task_instance import FlowRating
from . import practice_service


class PracticeServiceTest(TestCase):

    fixtures = ['instructions.json']

    def setUp(self):
        self.user = User.objects.create()

    def test_get_next_task_in_session(self):
        stored_task = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        TasksDifficultyModel.objects.create(task=stored_task)
        task_info = practice_service.get_next_task_in_session(student=self.user)
        self.assertIsNotNone(task_info)
        self.assertEquals('{"foo": "bar"}', task_info.task.workspace_settings)
        self.assertEquals('{}', task_info.task.maze_settings)
        self.assertEquals(TaskInstanceModel.objects.first().id,
                task_info.task_instance.pk)
        student = StudentModel.objects.get(user_id=self.user.pk)
        session = PracticeSession.objects.filter(student=student, active=True)[0]
        self.assertEquals(session, task_info.session)
        task_instance = TaskInstanceModel.objects.get(student=self.user)
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
        task_info = practice_service.get_task_by_id(student=self.user, task_id=stored_task.pk)
        self.assertIsNotNone(task_info)
        self.assertEquals('{"foo": "bar"}', task_info.task.workspace_settings)
        self.assertEquals('{}', task_info.task.maze_settings)
        self.assertEquals(TaskInstanceModel.objects.first().id,
                task_info.task_instance.pk)
        self.assertIsNone(task_info.session)

    def test_process_attempt_report(self):
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, solution_count=5)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=self.user,
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
        student = StudentModel.objects.get(user_id=self.user.pk)
        self.assertGreater(student.total_credits, 0)
        self.assertEqual(student.total_credits, student.free_credits)

    def test_process_flow_report_solved_task(self):
        difficulty_before_report = 1.0
        skill_before_report = -1.0
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, programming=difficulty_before_report)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=self.user, predicted_flow=-1.0)
        student = StudentModel.objects.create(user=self.user, programming=skill_before_report)
        practice_service.process_flow_report(
                student=self.user,
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
        TaskInstanceModel.objects.create(id=1, task_id=1, student=self.user, predicted_flow=1.0)
        student = StudentModel.objects.create(user=self.user, programming=1.0)
        skill_before_report = student.programming
        practice_service.process_giveup_report(
                student=self.user,
                task_instance_id=1,
                time_spent=987)
        task_instance = TaskInstanceModel.objects.get(id=1)
        self.assertEqual(task_instance.reported_flow, FlowRating.VERY_DIFFICULT)
        self.assertEqual(task_instance.time_spent, 987)
        skill_after_report = StudentModel.objects.get(user_id=student.pk).programming
        self.assertLess(skill_after_report, skill_before_report)

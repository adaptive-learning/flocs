"""Unit test of task service
"""

from django.contrib.auth.models import User
from django.test import TestCase
from tasks.models import TaskModel
from practice.models import StudentModel
from practice.models import TasksDifficultyModel
from practice.models import TaskInstanceModel
from practice.models.task_instance import FlowRating
from . import practice_service


class PracticeServiceTest(TestCase):

    fixtures = ['instructions.json']

    def setUp(self):
        self.student = User.objects.create()
        self.student_model = StudentModel.objects.create(user_id = self.student.pk)

    def test_get_next_task(self):
        stored_task = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        TasksDifficultyModel.objects.create(task=stored_task)
        retrieved_task = practice_service.get_next_task(student=self.student)
        self.assertIsNotNone(retrieved_task)
        self.assertEquals({"foo": "bar"}, retrieved_task['task']['workspace-settings'])
        self.assertEquals({}, retrieved_task['task']['maze-settings'])
        self.assertEquals(TaskInstanceModel.objects.first().id,
                retrieved_task['task-instance-id'])
        student_model = StudentModel.objects.get(user_id=self.student.pk)
        self.assertEquals(student_model.session.task_counter, retrieved_task['task_in_session'])

    def test_no_task_available(self):
        # if there are no tasks available, task_servise should raise
        # LookupError
        self.assertRaises(LookupError,
                practice_service.get_next_task, self.student)

    def test_get_task_by_id(self):
        stored_task = TaskModel.objects.create(maze_settings="{}",
                workspace_settings='{"foo": "bar"}')
        TasksDifficultyModel.objects.create(task=stored_task)
        retrieved_task = practice_service.get_task_by_id(student=self.student, task_id=stored_task.pk)
        self.assertIsNotNone(retrieved_task)
        self.assertEquals({"foo": "bar"}, retrieved_task['task']['workspace-settings'])
        self.assertEquals({}, retrieved_task['task']['maze-settings'])
        self.assertEquals(TaskInstanceModel.objects.first().id,
                retrieved_task['task-instance-id'])

    def test_process_attempt_report(self):
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, solution_count=5)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=self.student,
                predicted_flow=0.22)
        report = {
            "task-instance-id": 1,
            "task-id": 1,
            "attempt": 12,
            "solved": True,
            "given-up": False,
            "time": 234,
        }
        practice_service.process_attempt_report(self.student, report)
        difficulty = TasksDifficultyModel.objects.get(task_id=1)
        self.assertEquals(6, difficulty.solution_count)
        task_instance = TaskInstanceModel.objects.get(id=1)
        self.assertAlmostEquals(0.22, task_instance.predicted_flow)
        self.assertEquals(12, task_instance.attempt_count)
        self.assertEquals(234, task_instance.time_spent)

    def test_process_flow_report_solved_task(self):
        difficulty_before_report = 1.0
        skill_before_report = -1.0
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, programming=difficulty_before_report)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=self.student, predicted_flow=-1.0)
        student = StudentModel.objects.create(user=self.student, programming=skill_before_report)
        practice_service.process_flow_report(
                student=self.student,
                task_instance_id=1,
                given_up=False,
                reported_flow=FlowRating.EASY)
        task_instance = TaskInstanceModel.objects.get(id=1)
        skill_after_report = StudentModel.objects.get(user_id=student.pk).programming
        difficulty_after_report = TasksDifficultyModel.objects.get(task_id=1).programming
        self.assertEqual(task_instance.reported_flow, FlowRating.EASY)
        self.assertGreater(skill_after_report, skill_before_report)
        self.assertLess(difficulty_after_report, difficulty_before_report)

    def test_process_flow_report_given_up(self):
        TaskModel.objects.create(id=1)
        TasksDifficultyModel.objects.create(task_id=1, programming=-1.0)
        TaskInstanceModel.objects.create(id=1, task_id=1, student=self.student, predicted_flow=1.0)
        student = StudentModel.objects.create(user=self.student, programming=1.0)
        skill_before_report = student.programming
        practice_service.process_flow_report(
                student=self.student,
                task_instance_id=1,
                given_up=True)
        task_instance = TaskInstanceModel.objects.get(id=1)
        self.assertEqual(task_instance.reported_flow, FlowRating.VERY_DIFFICULT)
        skill_after_report = StudentModel.objects.get(user_id=student.pk).programming
        self.assertLess(skill_after_report, skill_before_report)

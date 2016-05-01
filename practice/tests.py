"""Tests of the practice app
"""

from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import TaskModel
from practice.models import StudentModel
from practice.models import PracticeSession
from practice.models import TaskInstanceModel
from practice.services import practice_session_service
from practice.services.practice_service import TaskInfo
from practice.views import task_info_to_json

class PracticeViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(user=self.user)
        self.task = TaskModel.objects.create(maze_settings="{}", workspace_settings='{}')
        self.instance1 = TaskInstanceModel.objects.create(task=self.task, student=self.student, solved=True)
        self.instance2 = TaskInstanceModel.objects.create(task=self.task, student=self.student, given_up=True)
        self.instance3 = TaskInstanceModel.objects.create(task=self.task, student=self.student)
        self.session = practice_session_service.create_session(self.instance1)
        self.toolbox = ['foo', 'bar']
        practice_session_service.next_task_in_session(self.student, self.instance2)
        practice_session_service.next_task_in_session(self.student, self.instance3)

    def test_task_info_to_json(self):
        task_info = TaskInfo(
            task_instance=self.instance3,
            task=self.task,
            new_instructions=None,
            all_instructions=None,
            session=self.session,
            toolbox=self.toolbox
        )
        json = task_info_to_json(task_info)
        self.assertEqual(len(json['session']['task-instances']), 3)
        self.assertEqual(json['session']['task-instances'][0]['solved'], True)
        self.assertEqual(json['session']['task-instances'][0]['given-up'], False)
        self.assertEqual(json['session']['task-instances'][1]['solved'], False)
        self.assertEqual(json['session']['task-instances'][1]['given-up'], True)
        self.assertEqual(json['session']['task-instances'][2]['solved'], False)
        self.assertEqual(json['session']['task-instances'][2]['given-up'], False)

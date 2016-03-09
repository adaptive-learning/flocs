from django.test import TestCase
from django.contrib.auth.models import User
from blocks.models import BlockModel
from practice.models import StudentModel
from practice.services.blocks import next_blocks_for_student, NoNextBlock
from practice.services.blocks import get_next_block_for_student


class BlocksServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(user=self.user)
        self.block1 = BlockModel.objects.create(name='b1', difficulty=0.1)
        self.block2 = BlockModel.objects.create(name='b2', difficulty=0.2)
        self.block3 = BlockModel.objects.create(name='b3', difficulty=0.3)
        self.block4 = BlockModel.objects.create(name='b4', difficulty=0.4)
        self.student.available_blocks = [self.block1, self.block3]
        self.student.save()

    def test_next_blocks_for_student(self):
        next_blocks = list(next_blocks_for_student(self.student))
        self.assertEquals(next_blocks, [self.block2, self.block4])

    def test_no_next_blocks_for_student(self):
        self.student.available_blocks = [self.block1, self.block2, self.block3, self.block4]
        self.student.save()
        next_blocks = list(next_blocks_for_student(self.student))
        self.assertEquals(next_blocks, [])

    def test_get_next_block_for_student(self):
        next_block = get_next_block_for_student(self.student)
        self.assertEqual(next_block, self.block2)

    def test_get_two_next_blocks_for_student(self):
        next_block = get_next_block_for_student(self.student)
        self.student.available_blocks.add(next_block)
        self.student.save()
        next_block2 = get_next_block_for_student(self.student)
        self.assertEqual(next_block2, self.block4)

    def test_get_next_block_for_student_all(self):
        self.student.available_blocks = [self.block1, self.block2, self.block3, self.block4]
        self.student.save()
        with self.assertRaises(NoNextBlock):
            get_next_block_for_student(self.student)

from django.test import TestCase
from django.contrib.auth.models import User
from blocks.models import BlockModel
from practice.models import StudentModel

from practice.services.purchases import buy_block, NotEnoughtCreditsException


class PurchasesServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.student = StudentModel.objects.create(
                user=self.user,
                free_credits=10, total_credits=50)
        self.block1 = BlockModel.objects.create(name='b1')
        self.block2 = BlockModel.objects.create(name='b2', price=2)
        self.block3 = BlockModel.objects.create(name='b3', price=10)
        self.block4 = BlockModel.objects.create(name='b4', price=20)
        self.student.available_blocks = [self.block1]
        self.student.save()

    def test_buy_block(self):
        buy_block(self.student, self.block2)
        self.assertEqual(set(self.student.available_blocks.all()), {self.block1, self.block2})
        self.assertEqual(self.student.free_credits, 8)
        self.assertEqual(self.student.total_credits, 50)

    def test_buy_block_db_changed(self):
        buy_block(self.student, self.block2)
        retrieved_student = StudentModel.objects.get(pk=self.student.pk)
        self.assertEqual(set(retrieved_student.available_blocks.all()), {self.block1, self.block2})
        self.assertEqual(retrieved_student.free_credits, 8)

    def test_buy_block_spending_all_credits(self):
        buy_block(self.student, self.block3)
        self.assertEqual(set(self.student.available_blocks.all()), {self.block1, self.block3})
        self.assertEqual(self.student.free_credits, 0)

    def test_attempt_to_buy_to_expensive_block(self):
        with self.assertRaises(NotEnoughtCreditsException):
            buy_block(self.student, self.block4)
        self.assertEqual(list(self.student.available_blocks.all()), [self.block1])
        self.assertEqual(self.student.free_credits, 10)

    def test_attempt_to_buy_already_owned_block(self):
        with self.assertRaises(ValueError):
            buy_block(self.student, self.block1)
        self.assertEqual(list(self.student.available_blocks.all()), [self.block1])
        self.assertEqual(self.student.free_credits, 10)

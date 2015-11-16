"""Unit test for math utils modul
"""

from django.test import TestCase
from decimal import Decimal

from .math import dict_product


class MathUtilsTest(TestCase):

    def test_dict_product(self):
        dict1 = {1: 20, 2: 0, 3:17, 4: 5, 5: 0.2}
        dict2 = {1: 1.5, 2: 0, 3:0, 4: 0.2, 5: 0.5}
        product = dict_product(dict1, dict2)
        self.assertAlmostEqual(31.1, product)


    def test_empty_dict_product(self):
        product = dict_product({}, {})
        self.assertAlmostEqual(0, product)

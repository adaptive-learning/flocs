from django.test import SimpleTestCase
from unittest import skipIf
from .credits import level_to_credits, compute_credits


class CreditsTest(SimpleTestCase):
    def test_at_least_one_credit(self):
        self.assertGreaterEqual(level_to_credits(1), 1)
        self.assertGreaterEqual(level_to_credits(5), 1)
        self.assertGreaterEqual(level_to_credits(10), 1)

    def test_level_to_credits_monoticity(self):
        result1 = level_to_credits(1)
        result2 = level_to_credits(2)
        result3 = level_to_credits(5)
        result4 = level_to_credits(10)
        self.assertGreaterEqual(result4, result3)
        self.assertGreaterEqual(result3, result2)
        self.assertGreaterEqual(result2, result1)

    def test_compute_credits_without_speed_bonus(self):
        ANY_LEVEL = 4
        LOW_PERCENTILE = 20
        earned_credits, speed_bonus = compute_credits(ANY_LEVEL, LOW_PERCENTILE)
        self.assertFalse(speed_bonus)
        self.assertEqual(earned_credits, level_to_credits(ANY_LEVEL))

    def test_compute_credits_with_speed_bonus(self):
        ANY_LEVEL = 4
        HIGH_PERCENTILE = 90
        earned_credits, speed_bonus = compute_credits(ANY_LEVEL, HIGH_PERCENTILE)
        self.assertTrue(speed_bonus)
        self.assertGreater(earned_credits, level_to_credits(ANY_LEVEL))

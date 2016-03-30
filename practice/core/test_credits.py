from django.test import SimpleTestCase
from unittest import skipIf
from .credits import difficulty_to_credits, compute_credits, MAX_CREDITS


class CreditsTest(SimpleTestCase):
    def test_at_least_one_credit(self):
        self.assertGreaterEqual(difficulty_to_credits(1), 1)
        self.assertGreaterEqual(difficulty_to_credits(0), 1)
        self.assertGreaterEqual(difficulty_to_credits(-1), 1)
        self.assertGreaterEqual(difficulty_to_credits(-10), 1)

    def test_difficulty_to_credits_monoticity(self):
        result1 = difficulty_to_credits(-5)
        result2 = difficulty_to_credits(-1)
        result3 = difficulty_to_credits(0)
        result4 = difficulty_to_credits(1)
        result5 = difficulty_to_credits(5)
        self.assertGreaterEqual(result5, result4)
        self.assertGreaterEqual(result4, result3)
        self.assertGreaterEqual(result3, result2)
        self.assertGreaterEqual(result2, result1)

    def test_difficulty_to_credits_extremes(self):
        self.assertEquals(difficulty_to_credits(-5), 1)
        self.assertEquals(difficulty_to_credits(-2), 1)
        self.assertEquals(difficulty_to_credits(2), MAX_CREDITS)
        self.assertEquals(difficulty_to_credits(5), MAX_CREDITS)

    def test_average_difficulty_to_credits(self):
        self.assertEquals(difficulty_to_credits(0), MAX_CREDITS / 2)
        self.assertEquals(difficulty_to_credits(-0.1), MAX_CREDITS / 2)

    @skipIf(True, 'prints overview table')
    def test_print_credits(self):
        print('||\nDifficulty -> Credits')
        for difficulty in [0.1 * n for n in range(-10, 11)]:
            print('{d:+.1f} -> {c}'.format(d=difficulty, c=difficulty_to_credits(difficulty)))
        print(difficulty_to_credits(-0.95), difficulty_to_credits(-0.88))

    def test_compute_credits_without_speed_bonus(self):
        ANY_DIFFICULTY = 0.5
        LOW_PERCENTILE = 20
        self.assertEquals(
            (difficulty_to_credits(ANY_DIFFICULTY), False),
            compute_credits(ANY_DIFFICULTY, LOW_PERCENTILE))

    def test_compute_credits_with_speed_bonus(self):
        ANY_DIFFICULTY = 0.5
        HIGH_PERCENTILE = 90
        earned_credits, speed_bonus = compute_credits(ANY_DIFFICULTY, HIGH_PERCENTILE)
        self.assertEquals(speed_bonus, True)
        self.assertGreater(earned_credits, difficulty_to_credits(ANY_DIFFICULTY))

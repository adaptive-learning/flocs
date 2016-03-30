from math import ceil
from common.utils.math import sigmoid

MAX_CREDITS = 10
SLOPE = 2.4
RELATIVE_SPEED_BONUS = 0.5
PERCENTIL_FOR_SPEED_BONUS = 70

def compute_credits(difficulty, speed_percentile):
    """
    Computes number of credits for solved task based on the difficulty of the
    task and percentile of solution speed.

    Return:
        - number of credits
        - whether speed bonus was obtained or not
    """
    assert isinstance(speed_percentile, int) # assumes number of percents
    credits = difficulty_to_credits(difficulty)
    speed_bonus = speed_percentile >= PERCENTIL_FOR_SPEED_BONUS
    if speed_bonus:
        credits += ceil(credits * RELATIVE_SPEED_BONUS)
    return credits, speed_bonus


def difficulty_to_credits(difficulty):
    """
    Convert task difficulty to the number of credits.
    Assumes that difficulty is approx. normally distributed around 0 with
    standard deviation approx. 1.
    """
    credits_value = sigmoid(SLOPE * difficulty) * MAX_CREDITS
    credits = ceil(credits_value)
    return credits

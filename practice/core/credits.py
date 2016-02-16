from math import ceil
from common.utils.math import sigmoid

MAX_CREDITS = 10
SLOPE = 2.4

def difficulty_to_credits(difficulty):
    """
    Convert task difficulty to the number of credits.
    Assumes that difficulty is approx. normally distributed around 0 with
    standard deviation approx. 1.
    """
    credits_value = sigmoid(SLOPE * difficulty) * MAX_CREDITS
    credits = ceil(credits_value)
    return credits

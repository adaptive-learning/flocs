from common.utils.activation import activation, AMPLITUDE
from math import ceil

MAX_CREDITS = 10

def difficulty_to_credits(difficulty):
    """
    Convert task difficulty to the number of credits.
    Assumes that difficulty is approx. normally distributed around 0 with
    standard deviation approx. 1.
    """
    credits_ratio = (activation(difficulty) + AMPLITUDE) / (2 * AMPLITUDE)
    credits = ceil(credits_ratio * MAX_CREDITS)
    return credits

from math import ceil


RELATIVE_SPEED_BONUS = 0.5
PERCENTIL_FOR_SPEED_BONUS = 70


def compute_credits(level, speed_percentile):
    """
    Computes number of credits for solved task based on the level of the
    task and percentile of solution speed.

    Return:
        - number of credits
        - whether speed bonus was obtained or not
    """
    assert isinstance(level, int)
    assert isinstance(speed_percentile, int) # assumes number of percents
    credits = level_to_credits(level)
    speed_bonus = speed_percentile >= PERCENTIL_FOR_SPEED_BONUS
    if speed_bonus:
        credits += ceil(credits * RELATIVE_SPEED_BONUS)
    return credits, speed_bonus


def level_to_credits(level):
    """ Convert level to the number of credits.
        Currently the relationship is an identity.
    """
    return level

import random


def weighted_choice(choices):
    """ Make a weighted random choice.

    Args:
        choices - list of tuples (weight, item)
    Return:
        random item
    """
    weights_sum = sum(weight for weight, item in choices)
    random_point = random.uniform(0, weights_sum)
    for weight, item in choices:
        random_point -= weight
        if random_point <= 0:
            break
    return item

"""
Math utilities
"""
from functools import reduce
from math import exp
import operator

def sigmoid(x):
    return 1 / (1 + exp(-x))

def dict_product(dict1, dict2):
    """
    Computes dot product of vectors represented by dictionaries.
    """
    assert dict1.keys() == dict2.keys()
    product = 0.0
    for key in dict1:
        product += dict1[key] * dict2[key]
    return product

def product(iterable):
    return reduce(operator.mul, iterable, 1)

def median(iterable):
    iterable = sorted(iterable)
    n = len(iterable)
    if n == 0:
        return 0
    elif n % 2 == 0:
        return (iterable[n//2 - 1] + iterable[n//2]) / 2
    else:
        return iterable[n//2]


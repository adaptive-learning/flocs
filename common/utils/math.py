"""
Math utilities
"""
from math import exp

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

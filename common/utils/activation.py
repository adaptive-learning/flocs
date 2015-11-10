"""
Utilities for activation function.
"""

from math import tanh


AMPLITUDE = 1.7159;
FREQUENCY = 0.6666667;


def activation(potential):
    """
    Compute activation function - hyperbolic tangent.
    """
    return AMPLITUDE * tanh(FREQUENCY * x);

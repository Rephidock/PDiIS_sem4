from random import random


def chance(chance_of_true: float) -> bool:
    """Returns true with a chance (float between 0 and 1, both inclusive)"""
    return random() < chance_of_true

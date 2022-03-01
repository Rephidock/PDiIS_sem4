from typing import Any
from random import random, randint


def chance(chance_of_true: float) -> bool:
    """Returns true with a chance (float between 0 and 1, both inclusive)"""
    return random() < chance_of_true


def list_pick_random(target: list) -> Any:
    """Returns a random item from the list"""
    if len(target) < 1:
        raise IndexError
    return target[randint(0, len(target))]

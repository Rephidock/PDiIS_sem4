from typing import Callable, Any
from queue import PriorityQueue
from enum import IntEnum


class StepPriority(IntEnum):

    # Lower value - higher priority

    PRE = 0
    LIFETIME = 1
    SPAWN = 2

    BEGIN = 10
    HUNGER = 15
    DISTRIBUTE = 17

    NORMAL = 20

    END = 30
    DECAY = 31
    MOVE = 32
    KILL = 35


class ActionPriorityQueue:
    """A priority queue of Callable actions"""

    __actions: PriorityQueue[tuple[StepPriority, Any, Callable[[Any], None]]]

    def __init__(self):
        self.__actions = PriorityQueue()

    def enqueue(self, priority: StepPriority, performer: Any, action: Callable[[Any], None]) -> None:
        """Enqueues an action with priority"""
        self.__actions.put((priority, performer, action))

    def perform(self) -> None:
        """Performs all actions from the queue, clearing the queue"""
        while not self.__actions.empty():
            item = self.__actions.get()
            item[2](item[1])

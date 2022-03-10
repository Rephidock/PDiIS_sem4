from typing import Callable, Any
from queue import PriorityQueue
from enum import IntEnum


class ActionPriority(IntEnum):
    """
    Base class for action priorities.
    Exists for annotations.
    Lower value - higher priority.
    """
    pass


class ActionPriorityQueue:
    """A priority queue of Callable actions"""

    __actions: PriorityQueue[tuple[ActionPriority, Any, Callable[[Any], None]]]

    def __init__(self):
        self.__actions = PriorityQueue()

    def enqueue(self, priority: ActionPriority, performer: Any, action: Callable[[Any], None]) -> None:
        """Enqueues an action with priority"""
        self.__actions.put((priority, performer, action))

    def perform(self) -> None:
        """Performs all actions from the queue, clearing the queue"""
        while not self.__actions.empty():
            item = self.__actions.get()
            item[2](item[1])

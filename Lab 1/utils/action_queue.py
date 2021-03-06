from typing import Callable
from queue import PriorityQueue
from enum import IntEnum
from dataclasses import dataclass, field


class ActionPriority(IntEnum):
    """
    Base class for action priorities.
    Exists for annotations.
    Lower value - higher priority.
    """
    pass


@dataclass(order=True)
class ActionPriorityItem:
    priority: ActionPriority = field()
    action: Callable[[], None] = field(compare=False)
    pass


class ActionPriorityQueue:
    """A priority queue of Callable actions"""

    __actions: PriorityQueue[ActionPriorityItem]

    def __init__(self):
        self.__actions = PriorityQueue()

    def enqueue(self, priority: ActionPriority, action: Callable[[], None]) -> None:
        """Enqueues an action with priority"""
        self.__actions.put(ActionPriorityItem(priority, action))

    def perform(self) -> None:
        """Performs all actions from the queue, clearing the queue"""
        while not self.__actions.empty():
            self.__actions.get().action()

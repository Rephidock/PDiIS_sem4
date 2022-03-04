from __future__ import annotations
from zeroplayer.entity_killable import EntityKillable
from zeroplayer.action_queue import StepPriority, ActionPriorityQueue


class Resource(EntityKillable):

    # Class
    _threshold: float = 0
    _decay: float = 0

    # Instance
    _value: float

    def __init__(self, initial_value: float):
        super().__init__()
        self._value = initial_value

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.DECAY, self, self.__handle_decay)
        queue.enqueue(StepPriority.DECAY, self, self.__handle_exhaustion)
        super().step(queue)

    def take(self, value: float) -> None:
        self._value -= value

    def __handle_decay(self) -> None:
        self._value -= self.__class__._decay

    def __handle_exhaustion(self) -> None:
        # Check resource value
        if self._value <= self.__class__._threshold:
            self.kill()

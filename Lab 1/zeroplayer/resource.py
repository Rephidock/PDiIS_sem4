from __future__ import annotations
from typing import Callable
from dataclasses import dataclass
from zeroplayer.entity import Entity
from zeroplayer.entity_killable import EntityKillable
from zeroplayer.action_queue import StepPriority, ActionPriorityQueue


class Resource(EntityKillable):

    # Class
    _threshold: float = 0
    _decay: float = 0

    # Instance
    _value: float
    _requests: list[ResourceRequest]

    def __init__(self, initial_value: float):
        super().__init__()
        self._value = initial_value
        self._requests = list()

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.DISTRIBUTE, self, self.__handle_distribution)
        queue.enqueue(StepPriority.DECAY, self, self.__handle_decay)
        queue.enqueue(StepPriority.DECAY, self, self.__handle_exhaustion)
        super().step(queue)

    def sign(self, taker: Entity, value: float, receiver: Callable) -> None:
        self._requests.append(ResourceRequest(taker, value, receiver))

    def __handle_distribution(self) -> None:
        # Find total of requests value
        total_val = 0.0
        for request in self._requests:
            total_val += request.value

        # Get multiplier for distribution
        mult = min(1.0, self._value/total_val)

        # Distribute
        for request in self._requests:
            self._value -= mult * request.value
            request.receiver(mult * request.value)

    def __handle_decay(self) -> None:
        self._value -= self._decay

    def __handle_exhaustion(self) -> None:
        # Check resource value
        if self._value <= self.__class__._threshold:
            self.kill()


@dataclass
class ResourceRequest:
    taker: Entity
    value: float
    receiver: Callable[[float], None]

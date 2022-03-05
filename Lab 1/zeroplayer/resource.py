from __future__ import annotations
from typing import Callable
from dataclasses import dataclass
from zeroplayer.entity import Entity
from zeroplayer.entity_killable import EntityKillable
from zeroplayer.action_queue import StepPriority, ActionPriorityQueue


class Resource(EntityKillable):
    """
    Represents a finite resource.
    Resource may decay over time and accelerate.

    Class settings:
      - _death_threshold = 0.0
      - _decay_speed_start = 0.0
      - _decay_acceleration = 0.0
    """

    # Class
    _death_threshold: float = 0.0
    _decay_speed_start: float = 0.0
    _decay_acceleration: float = 0.0

    # Instance
    __value: float
    __requests: list[ResourceRequest]
    _decay_speed: float

    def __init__(self, initial_value: float):
        super().__init__()
        self.__value = initial_value
        self.__requests = list()
        self._decay_speed = self._decay_speed_start

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.DISTRIBUTE, self, self.__handle_distribution)
        queue.enqueue(StepPriority.DECAY, self, self.__handle_decay)
        queue.enqueue(StepPriority.DECAY, self, self.__handle_exhaustion)
        super().step(queue)

    def sign(self, taker: Entity, value: float, receiver: Callable[[Entity, float], None]) -> None:
        self.__requests.append(ResourceRequest(taker, value, receiver))

    def __handle_distribution(self) -> None:
        # Find total of requests value
        total_val = 0.0
        for request in self.__requests:
            total_val += request.value

        # Get multiplier for distribution
        mult = min(1.0, self.__value/total_val)

        # Distribute
        for request in self.__requests:
            self.__value -= mult * request.value
            request.receiver(request.taker, mult * request.value)

        # Clear
        self.__requests.clear()

    def __handle_decay(self) -> None:
        self.__value -= self._decay_speed
        self._decay_speed += self._decay_acceleration

    def __handle_exhaustion(self) -> None:
        # Check resource value
        if self.__value <= self._death_threshold:
            self.kill()


@dataclass
class ResourceRequest:
    taker: Entity
    value: float
    receiver: Callable[[Entity, float], None]

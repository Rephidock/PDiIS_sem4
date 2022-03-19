from __future__ import annotations
from typing import Callable, Type
from utils.action_queue import ActionPriorityQueue

from dataclasses import dataclass
from zeroplayer.entities.entity_killable import EntityKillable
from zeroplayer.step_priorities import StepPriority


class Resource(EntityKillable):
    """
    Represents a finite resource.
    Resource may decay over time and the day may accelerate.

    Class attributes:
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
    __decay_speed: float

    def __init__(self, initial_value: float):
        super().__init__()
        self.__value = initial_value
        self.__requests = list()
        self.__decay_speed = self._decay_speed_start

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.DISTRIBUTE, self.__handle_distribution)
        queue.enqueue(StepPriority.DECAY, self.__handle_decay)
        queue.enqueue(StepPriority.DECAY, self.__handle_exhaustion)
        super().step(queue)

    #region //// Distribution

    def sign(self, value: float, receive_handle: Callable[[float], None]) -> None:
        self.__requests.append(ResourceRequest(value, receive_handle))

    def __handle_distribution(self) -> None:

        # Skip if no one requested
        if len(self.__requests) < 1:
            return

        # Find total of requests value
        total_val = 0.0
        for request in self.__requests:
            total_val += request.value

        # Get multiplier for distribution
        mult = min(1.0, self.__value/total_val)

        # Distribute
        for request in self.__requests:
            self.__value -= mult * request.value
            request.receive_handle(mult * request.value, type(self))

        # Clear
        self.__requests.clear()

    #endregion

    #region //// Value, decay

    @property
    def value(self) -> float:
        return self.__value

    @property
    def decay_speed(self) -> float:
        return self.__decay_speed

    def __handle_decay(self) -> None:
        self.__value -= self.__decay_speed
        self.__decay_speed += self._decay_acceleration

    def __handle_exhaustion(self) -> None:
        # Check resource value
        if self.__value <= self._death_threshold:
            self.kill()

    #endregion


@dataclass
class ResourceRequest:
    value: float
    receive_handle: Callable[[float, Type[Resource]], None]

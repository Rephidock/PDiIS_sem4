from __future__ import annotations
from typing import Optional, Type
from zeroplayer.entity_movable import EntityMovable
from zeroplayer.entity_killable import EntityKillable
from zeroplayer.resource import Resource
from zeroplayer.action_queue import StepPriority, ActionPriorityQueue


class Creature(EntityKillable, EntityMovable):

    # Aging
    _max_lifetime: Optional[int] = None

    # Hunger
    _starting_satiety: float = 0.8
    _hunger_rate: float = 0.1
    _sated_threshold: float = 0.4  # 0.0 - 1.0

    # Eating
    _desired_resource: Type[Resource] = Resource
    _resource_intake_mult: float = 1.0

    # Instance variables
    _satiety: float  # 0.0-1.0

    def __init__(self):
        super().__init__()
        self._satiety = self._starting_satiety

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.HUNGER, self, self.__handle_hunger)
        queue.enqueue(StepPriority.DECAY, self, self.__handle_death_age)
        queue.enqueue(StepPriority.DECAY, self, self.__handle_death_starvation)
        super().step(queue)

    def _eat(self) -> None:
        """Called when hungry"""
        self._find_food(1.5 * self._hunger_rate)

    def _find_food(self, desired_amount: float):
        """
        Signs the creature for desired resource distribution
        from all neighbouring resource entities.
        """
        # Sign for distribution
        resources = self.parent.children_by_type(self._desired_resource)
        requested_amount = desired_amount/len(resources)
        for resource in resources:
            resource.sign(self, requested_amount, self._resource_intake)

    def _resource_intake(self, value: float):
        """Passed into resource distribution as the receiver method"""
        self._satiety += value * self._resource_intake_mult

    def __handle_hunger(self) -> None:
        # Hunger
        self._satiety -= self._hunger_rate

        # Eating
        if self._satiety <= self._sated_threshold:
            self._eat()

    def __handle_death_age(self) -> None:
        if (self._max_lifetime is not None) and (self.lifetime >= self._max_lifetime):
            self.kill()

    def __handle_death_starvation(self) -> None:
        if self._satiety <= 0:
            self.kill()

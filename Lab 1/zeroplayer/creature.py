from __future__ import annotations
from typing import Optional, Type, Callable
from zeroplayer.entity_movable import EntityMovable
from zeroplayer.entity_killable import EntityKillable
from zeroplayer.resource import Resource
from zeroplayer.action_queue import StepPriority, ActionPriorityQueue


class Creature(EntityKillable, EntityMovable):

    # Class variables
    _max_lifetime: Optional[int] = None
    _starting_satiety: float = 0.8
    _hunger_rate: float = 0.1
    _sated_threshold: float = 0.4  # 0.0 - 1.0

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
        pass

    def _sign_to_resource_distribution(
            self,
            resource_type: Type[Resource],
            desired_amount: float,
            receiver: Optional[Callable[[Creature, float], None]] = None
    ):
        """
        Signs the creature for resource distribution
        from all entities of a set type.

        If receiver is None it is replaced with resource_intake
        """
        # Default Receiver
        if receiver is None:
            receiver = self._resource_intake

        # Sign for distribution
        resources = self.parent.children_by_type(resource_type)
        requested_amount = desired_amount/len(resources)
        for resource in resources:
            resource.sign(self, requested_amount, receiver)

    def _resource_intake(self, value: float):
        self._satiety += value

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

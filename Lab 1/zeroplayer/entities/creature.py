from __future__ import annotations
from typing import Optional, Type
from utils.action_queue import ActionPriorityQueue
from utils.rand_ext import chance
from utils.math import lerp_clamped
from enum import Enum
from dataclasses import dataclass

from zeroplayer.entities.entity_movable import EntityMovable
from zeroplayer.entities.entity_killable import EntityKillable
from zeroplayer.entities.resource import Resource
from zeroplayer.spawn_rule import SpawnRule
from zeroplayer.step_priorities import StepPriority


class Creature(EntityKillable, EntityMovable):
    """
    Represents a living creature.
    A creature needs nutrition, can die of starvation and age, can procreate.

    Class attributes:
      - _max_lifetime = None

      - _satiety_starting = 0.8
      - _satiety_hunger_rate = 0.1
      - _satiety_sated_threshold = 0.4

      - _intake_rules = dict()

      - _procreation_male_threshold = 1
      - _procreation_spawn_count = 1
      - _procreation_female_chance = 0.5
      - _procreation_spawn_rules = ()
    """

    # Aging
    _max_lifetime: Optional[int] = None

    # Hunger
    _satiety_starting: float = 0.8
    _satiety_hunger_rate: float = 0.1
    _satiety_stuffed_threshold: float = 0.4  # 0.0 - 1.0

    # Eating
    _intake_rules: dict[Type[Resource], IntakeRule] = dict()

    # Procreation
    _procreation_male_threshold: int = 1
    _procreation_spawn_count: int = 1
    _procreation_female_chance: float = 0.5  # 0.0 - 1.0
    _procreation_spawn_rules: tuple[SpawnRule] = ()

    # Instance variables
    _satiety: float  # 0.0-1.0
    gender: Gender

    def __init__(self, forced_gender: Optional[Gender] = None):
        super().__init__()
        self._satiety = self._satiety_starting

        if forced_gender is None:
            self.gender = Gender.FEMALE if chance(self._procreation_female_chance) else Gender.MALE
        else:
            self.gender = forced_gender

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.HUNGER, self.__handle_hunger)
        queue.enqueue(StepPriority.DECAY, self.__handle_death_age)
        queue.enqueue(StepPriority.DECAY, self.__handle_death_starvation)
        queue.enqueue(StepPriority.SPAWN, self.__handle_procreation)
        super().step(queue)

    #region //// Satiety and intake

    @property
    def satiety(self) -> float:
        return self._satiety

    def __handle_hunger(self) -> None:

        # Eating
        if self._satiety <= self._satiety_stuffed_threshold:
            self._intake()

        # Hunger
        self._satiety -= self._satiety_hunger_rate

    def __handle_death_starvation(self) -> None:
        if self._satiety <= 0:
            self.kill()

    def _intake(self) -> None:
        """Called when hungry"""
        self._request_food(self._search_food())

    def _search_food(self) -> list[Resource]:
        """Returns a list of desired intake resource entities."""
        intake_resource_type = [key for key in self._intake_rules.keys()]
        return self.parent.children_by_type(*intake_resource_type)

    def _request_food(self, food_sources: list[Resource]) -> None:
        """Signs the creature for resource distribution."""
        for resource, amount in zip(food_sources, self._request_get_values(food_sources)):
            resource.sign(amount, self._receive_resource)

    def _request_get_values(self, food_sources: list[Resource]) -> list[float]:
        """Returns meal size for each food source based on current satiety"""

        # Get weights
        weight_sum = 0
        for source in food_sources:
            weight_sum += self._intake_rules[type(source)].request_weight

        # Get values
        values = [
            lerp_clamped(
                self._intake_rules[type(source)].request_starved,
                self._intake_rules[type(source)].request_stuffed,
                self._satiety / self._satiety_stuffed_threshold
            )
            * self._intake_rules[type(source)].request_weight / weight_sum
            for source in food_sources
        ]

        return values

    def _receive_resource(self, value: float, type_: Type[Resource]) -> None:
        """Passed into resource distribution as receive_handle"""
        self._satiety += value * self._intake_rules[type_].value_mult

    #endregion

    #region //// Age and procreation

    def __handle_death_age(self) -> None:
        if (self._max_lifetime is not None) and (self.lifetime >= self._max_lifetime):
            self.kill()

    def __handle_procreation(self) -> None:

        # Gender check
        if self.gender != Gender.FEMALE:
            return

        # Threshold check
        if len(
            list(
                filter(
                    lambda child: child.gender == Gender.MALE,
                    self.parent.children_by_type(type(self))
                )
            )
        ) < self._procreation_male_threshold:
            return

        # Spawn children
        for _ in range(self._procreation_spawn_count):
            for rule in self._procreation_spawn_rules:
                rule.spawn_as_child(self.parent)

    #endregion


class Gender(Enum):
    MALE = 0
    FEMALE = 1


@dataclass
class IntakeRule:
    value_mult: float
    request_stuffed: float
    request_starved: float
    request_weight: int = 1

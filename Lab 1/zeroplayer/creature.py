from __future__ import annotations
from typing import Optional, Type
from enum import Enum
from utils.rand_ext import chance
from utils.math import lerp_clamped

from zeroplayer.entity_movable import EntityMovable
from zeroplayer.entity_killable import EntityKillable
from zeroplayer.resource import Resource
from zeroplayer.spawn_rule import SpawnRule
from zeroplayer.action_queue import StepPriority, ActionPriorityQueue


class Creature(EntityKillable, EntityMovable):
    """
    Represents a living creature.
    A creature needs nutrition, can die of starvation and age, can procreate.

    Class settings:
      - _max_lifetime = None

      - _satiety_starting = 0.8
      - _satiety_hunger_rate = 0.1
      - _satiety_sated_threshold = 0.4

      - _intake_resource_type = Resource
      - _intake_value_mult = 1.0
      - _intake_request_stuffed = 1.0
      - _intake_request_starved = 1.0

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
    _satiety_sated_threshold: float = 0.4  # 0.0 - 1.0

    # Eating
    _intake_resource_type: Type[Resource] = Resource
    _intake_value_mult: float = 1.0
    _intake_request_stuffed: float = 1.0
    _intake_request_starved: float = 1.0

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
        queue.enqueue(StepPriority.HUNGER, self, self.__handle_hunger)
        queue.enqueue(StepPriority.DECAY, self, self.__handle_death_age)
        queue.enqueue(StepPriority.DECAY, self, self.__handle_death_starvation)
        queue.enqueue(StepPriority.SPAWN, self, self.__handle_procreation)
        super().step(queue)

    #region //// Eating logic

    def __handle_hunger(self) -> None:

        # Eating
        if self._satiety <= self._satiety_sated_threshold:
            self._intake()

        # Hunger
        self._satiety -= self._satiety_hunger_rate

    def __handle_death_starvation(self) -> None:
        if self._satiety <= 0:
            self.kill()

    def _intake(self) -> None:
        """Called when hungry"""
        self._request_food(self._search_food(), self._food_size())

    def _search_food(self) -> list[Resource]:
        """Returns a list of desired intake resource entities."""
        return self.parent.children_by_type(self._intake_resource_type)

    def _food_size(self) -> float:
        """Returns meal size based on current satiety"""
        return lerp_clamped(
                self._intake_request_starved,
                self._intake_request_stuffed,
                self._satiety / self._satiety_sated_threshold
            )

    def _request_food(self, food_sources: list[Resource], desired_amount: float) -> None:
        """Signs the creature for resource distribution."""
        requested_amount = desired_amount/len(food_sources)
        for resource in food_sources:
            resource.sign(self, requested_amount, self._receive_resource)

    def _receive_resource(self, value: float) -> None:
        """Passed into resource distribution as receive_handle"""
        self._satiety += value * self._intake_value_mult

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

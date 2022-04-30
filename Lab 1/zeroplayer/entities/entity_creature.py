from __future__ import annotations
from typing import TYPE_CHECKING, Generator, Type, cast

from utils.action_queue import ActionPriorityQueue
from utils.exceptions import InvalidOperationError
import utils.activator as activator
from utils.rand_ext import chance
from random import choice
from abc import ABCMeta

from zeroplayer.step_priorities import StepPriority
from zeroplayer.entities.entity_hunter import EntityHunter
from zeroplayer.entities.entity_decaying import EntityDecaying

# annotations
if TYPE_CHECKING:
    from zeroplayer.entities.entity_killable import EntityKillable
    from zeroplayer.snapshotable import Snapshot


class EntityCreature(EntityHunter, EntityDecaying, metaclass=ABCMeta):
    """
    An EntityHunter with a max lifetime, procreation, and hunger as integrity
    """

    #region //// Init

    _max_lifetime: int

    _satiety_multipliers: dict[Type[EntityKillable], float] = {}

    _procreation_chance: float = 0.5  # 0 <= value <= 1
    _procreation_cooldown: int = 5
    __procreation_current_cooldown: int

    def __init__(self):
        self.__procreation_current_cooldown = self._procreation_cooldown
        super().__init__()

    #endregion

    #region //// Step

    def step(self, action_queue: ActionPriorityQueue) -> None:
        super().step(action_queue)
        action_queue.enqueue(StepPriority.AGE, self.__action_age)
        action_queue.enqueue(StepPriority.PROCREATION, self.__action_procreate)

    #endregion

    #region //// Max lifetime

    def __action_age(self):
        if self.lifetime > self._max_lifetime:
            self.kill()

    #endregion

    #region //// Hunger

    @property
    def satiety(self) -> float:
        return self.integrity

    def eat(self, satiety: float):
        self.repair(satiety)

    def leap_process_prey(self, target: EntityKillable):
        # Get mult
        mult = self._satiety_multipliers.get(type(target), 0.0)

        # Get value
        value = 1.0
        if isinstance(target, EntityCreature):
            value = cast(EntityCreature, target).satiety
        elif isinstance(target, EntityDecaying):
            value = cast(EntityDecaying, target).integrity

        # Add satiety
        self.eat(mult*value)

    #endregion

    #region //// Procreation

    def __action_procreate(self):

        # Killed guard
        if self.is_killed: return

        # Location guard
        if self.location is None:
            raise InvalidOperationError("Cannot procreate when not on location")

        # Cooldown
        if self.__procreation_current_cooldown > 0:
            self.__procreation_current_cooldown -= 1
            return

        # Spawn with chance
        if chance(self._procreation_chance):

            # Get valid spawn position
            spawn_positions = list(
                                filter(
                                    lambda pos: self.location.position_empty(*pos),
                                    self.get_allowed_spawn_destinations()
                                )
                            )

            # Spawn at random valid position
            if len(spawn_positions) > 0:
                spawn_x, spawn_y = choice(spawn_positions)
                child = cast(type(self), activator.create_instance(type(self), ()))  # Create
                child.place_at(self.location, spawn_x, spawn_y)  # Move
                child.integrity = self.satiety  # Set satiety

        # Reset cooldown
        self.__procreation_current_cooldown = self._procreation_cooldown

    @staticmethod
    def get_allowed_spawn_shifts() -> Generator[tuple[int, int], None, None]:
        """
        Virtual.
        Returns relative to self displacements (dx, dy)
        where a child can spawn.
        """

        # Horizontal one space
        yield -1, 0
        yield 1, 0
        # Vertical one spaces
        yield 0, -1
        yield 0, 1

    def get_allowed_spawn_destinations(self) -> Generator[tuple[int, int], None, None]:
        for dx, dy in self.get_allowed_spawn_shifts():
            yield self.location.clamp_position(self.x + dx, self.y + dy)

    #endregion

    #region //// Snapshot

    def fill_snapshot(self, snapshot: Snapshot):
        snapshot.set_data(EntityCreature, "procreation_cd", self.__procreation_current_cooldown)
        super().fill_snapshot(snapshot)

    def restore_from_snapshot(self, snapshot: Snapshot):
        super().restore_from_snapshot(snapshot)
        self.__procreation_current_cooldown = snapshot.get_data(EntityCreature, "procreation_cd")

    #endregion

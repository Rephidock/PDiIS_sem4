from __future__ import annotations
from typing import Generator, cast

from utils.action_queue import ActionPriorityQueue
from utils.exceptions import InvalidOperationError
from abc import ABCMeta, abstractmethod
from random import randint

from zeroplayer.step_priorities import StepPriority
from zeroplayer.entities.entity_killable import EntityKillable
from zeroplayer.entities.entity_moving import EntityMoving


class EntityHunter(EntityMoving, metaclass=ABCMeta):
    """
    An Entity that wanders and searches for other entities
    and leaps towards targets, killing them.
    Can only kill EntityKillable
    """

    #region //// Init

    _vision_distance: int = 4  # For default vision

    _prey_types: tuple[EntityKillable, ...] = ()
    _leap_distance: float = 1.5  # Actual max distance for leaps
    __has_leaped: bool
    __leap_x: int
    __leap_y: int

    def __init__(self):
        self.__has_leaped = False
        self.__leap_x = 0
        self.__leap_y = 0
        super().__init__()

    #endregion

    #region //// Step

    def step(self, action_queue: ActionPriorityQueue) -> None:
        super().step(action_queue)
        action_queue.enqueue(StepPriority.LEAP_ATTACK, self.__action_leap_attack)
        action_queue.enqueue(StepPriority.SEARCH, self.__action_search)
        action_queue.enqueue(StepPriority.WANDER, self.__action_wander)
        action_queue.enqueue(StepPriority.LEAP_MOVE, self.__action_leap_move)

    #endregion

    #region //// Searching, wandering

    def __action_search(self):
        if self.location is None:
            raise InvalidOperationError("Cannot search when not on location")

        # Look around
        for dest_x, dest_y in self.get_vision_destinations():
            # If prey is seen
            if type(self.location.entity_at_position(dest_x, dest_y)) in self._prey_types:
                # Switch attention to it if it is closer
                has_changed_target = self.set_move_target_if_closer(dest_x, dest_y)
                if has_changed_target: continue
                # Switch attention to it if currently chasing None
                if self.entity_at_move_target() is None:
                    self.set_move_target(dest_x, dest_y)

    def __action_wander(self):
        if self.location is None:
            raise InvalidOperationError("Cannot search when not on location")

        # Leap cancels wander
        if self.__has_leaped: return

        # Wander if there is no search target
        if self.has_move_target(): return

        # Move to random location
        self.set_move_target(
            randint(0, self.location.width - 1),
            randint(0, self.location.height - 1)
        )

    #endregion

    #region //// Vision

    @classmethod
    def get_vision_shifts(cls) -> Generator[tuple[int, int], None, None]:
        """
        Virtual.
        Returns relative displacements (dx, dy) this entity can see.
        """
        for xx in range(-cls._vision_distance, cls._vision_distance+1):
            for yy in range(-cls._vision_distance, cls._vision_distance+1):
                if xx != 0 or yy != 0:
                    yield xx, yy

    def get_vision_destinations(self) -> Generator[tuple[int, int], None, None]:
        for dx, dy in self.get_vision_shifts():
            yield self.location.clamp_position(self.x + dx, self.y + dy)

    #endregion

    #region //// Leap

    def __action_leap_attack(self):
        # Reset leap
        self.__has_leaped = False

        # Can only leap at move target
        if not self.has_move_target(): return

        # Check distance
        if self.distance_to_target() > self._leap_distance: return  # Target must be within leap range

        # Check target
        prey = self.entity_at_move_target()
        if type(prey) not in self._prey_types: return     # Target must have a targeted type
        if not isinstance(prey, EntityKillable): return   # Target must be EntityKillable
        if cast(EntityKillable, prey).is_killed: return   # Target must be still alive

        # Perform leap attack
        cast(EntityKillable, prey).kill(no_residue=True)
        self.__has_leaped = True
        self.__leap_x, self.__leap_y = self.get_move_target_position()
        self.remove_move_target()
        self.leap_process_prey(prey)

    def __action_leap_move(self):
        if not self.__has_leaped: return
        if self.is_killed: return
        self.move_to_instant(self.__leap_x, self.__leap_y)

    @abstractmethod
    def leap_process_prey(self, target: EntityKillable):
        """
        Abstract. Virtual.
        Called after successful leap attack.
        """
        pass

    #endregion

from __future__ import annotations
from typing import TYPE_CHECKING, Generator

from utils.action_queue import ActionPriorityQueue
from utils.exceptions import InvalidOperationError
from abc import ABCMeta
from dataclasses import dataclass
import math

from zeroplayer.step_priorities import StepPriority
from zeroplayer.entities.entity_killable import EntityKillable

# annotations
if TYPE_CHECKING:
    from zeroplayer.entities.entity import Entity
    from zeroplayer.snapshotable import Snapshot


class EntityMoving(EntityKillable, metaclass=ABCMeta):
    """An Entity that can move over time"""

    #region //// Init

    __target: MovementTarget | None

    def __init__(self):
        self.__target = None

        super().__init__()

    #endregion

    #region //// Step

    def step(self, action_queue: ActionPriorityQueue) -> None:
        super().step(action_queue)
        action_queue.enqueue(StepPriority.MOVE, self.advance_to_target_instant)

    #endregion

    #region //// Instant movement

    def move_to_instant(self, x: int, y: int) -> bool:
        """
        Moves self to a position if it is not occupied.
        Returns True if movement was successful.
        """
        if self.location is None:
            raise InvalidOperationError("Cannot move when not on location")

        # Killed entities don't move
        if self.is_killed: return False

        # Only move to free space
        if not self.location.position_empty(x, y): return False

        self.place_at(self.location, x, y)
        return True

    def advance_to_target_instant(self):
        if not self.has_move_target(): return

        # Killed entities don't move
        if self.is_killed: return

        # Check if at target
        if self.is_at_target():
            self.remove_move_target()
            return

        # Get and sort dest-s by distance to target
        destinations = list(self.get_shift_destinations())
        destinations.sort(key=lambda dest: self.__target.distance_from(*dest))

        # Goto first unoccupied
        for new_x, new_y in destinations:
            if self.move_to_instant(new_x, new_y): break

        # Check if at target
        if self.is_at_target():
            self.remove_move_target()

    #endregion

    #region //// Target

    def set_move_target(self, x: int, y: int):
        """Sets move target for current entity"""

        if self.location is None:
            raise InvalidOperationError("Cannot set move target when not on location")

        x, y = self.location.clamp_position(x, y)
        self.__target = MovementTarget(x, y)

    def set_move_target_if_closer(self, x: int, y: int) -> bool:
        """
        Sets move target for current entity if it is closer
        Returns True if target was change
        """

        if self.location is None:
            raise InvalidOperationError("Cannot set move target when not on location")

        if not self.has_move_target():
            self.set_move_target(x, y)
            return True

        # Pick closer of the 2
        x, y = self.location.clamp_position(x, y)
        new_dist = MovementTarget.distance_2d(self.x, self.y, x, y)
        if new_dist < self.distance_to_target():
            self.set_move_target(x, y)
            return True

        return False

    def get_move_target_position(self) -> tuple[int, int]:
        return self.__target.x, self.__target.y

    def entity_at_move_target(self) -> Entity | None:
        if not self.has_move_target(): return None
        return self.location.entity_at_position(self.__target.x, self.__target.y)

    def has_move_target(self) -> bool:
        return self.__target is not None

    def remove_move_target(self):
        self.__target = None

    def is_at_target(self) -> bool:
        return self.x == self.__target.x and self.y == self.__target.y

    def distance_to_target(self) -> float:
        return self.__target.distance_from(self.x, self.y)

    #endregion

    #region //// Shifts

    @classmethod
    def get_allowed_shifts(cls) -> Generator[tuple[int, int], None, None]:
        """
        Virtual.
        Returns relative displacements (dx, dy) this entity can perform per step.
        One of the steps listed must be performed during movement unless
        all possible spaces are occupied.
        """

        # Allow standing still
        yield 0, 0
        # Horizontal one space
        yield -1, 0
        yield 1, 0
        # Vertical one spaces
        yield 0, -1
        yield 0, 1

    def get_shift_destinations(self) -> Generator[tuple[int, int], None, None]:
        for dx, dy in self.get_allowed_shifts():
            yield self.location.clamp_position(self.x + dx, self.y + dy)

    #endregion

    #region //// Snapshot

    def fill_snapshot(self, snapshot: Snapshot):
        coords = list(self.get_move_target_position()) if self.has_move_target() else None
        snapshot.set_data(EntityMoving, "move_target", coords)
        super().fill_snapshot(snapshot)

    def restore_from_snapshot(self, snapshot: Snapshot):
        super().restore_from_snapshot(snapshot)
        coords = snapshot.get_data(EntityMoving, "move_target")
        if coords is None:
            self.remove_move_target()
        else:
            self.set_move_target(*coords)

    #endregion


@dataclass
class MovementTarget:
    x: int = 0
    y: int = 0

    def distance_from(self, start_x: int, start_y: int) -> float:
        return self.distance_2d(start_x, start_y, self.x, self.y)

    @staticmethod
    def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
        return math.hypot(x2 - x1, y2 - y1)

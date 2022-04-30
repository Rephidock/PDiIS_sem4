from __future__ import annotations
from typing import TYPE_CHECKING

from utils.action_queue import ActionPriorityQueue
from utils.math import clamp
from abc import ABCMeta

from zeroplayer.step_priorities import StepPriority
from zeroplayer.entities.entity_killable import EntityKillable

# annotations
if TYPE_CHECKING:
    from zeroplayer.snapshotable import Snapshot


class EntityDecaying(EntityKillable, metaclass=ABCMeta):
    """An Entity that can be killed"""

    #region //// Init

    __integrity: float
    _integrity_cap: float = 1.0
    _integrity_start: float = 1.0
    _decay_speed: float = 0.1

    def __init__(self):
        self.__integrity = self._integrity_start
        super().__init__()

    #endregion

    #region //// Step

    def step(self, action_queue: ActionPriorityQueue) -> None:
        super().step(action_queue)
        action_queue.enqueue(StepPriority.DECAY, self.__action_decay)

    #endregion

    #region //// Decay, Integrity

    def __action_decay(self):
        self.__integrity -= self._decay_speed
        if self.__integrity <= 0:
            self.kill()

    def repair(self, delta_integrity: float):
        self.__integrity = min(self._integrity_cap, self.__integrity + delta_integrity)

    @property
    def integrity(self) -> float:
        return self.__integrity

    @integrity.setter
    def integrity(self, value: float):
        self.__integrity = clamp(value, 0, self._integrity_cap)

    @property
    def integrity_cap(self) -> float:
        return self._integrity_cap

    #endregion

    #region //// Snapshot

    def fill_snapshot(self, snapshot: Snapshot):
        snapshot.set_data(EntityDecaying, "integrity", self.__integrity)
        super().fill_snapshot(snapshot)

    def restore_from_snapshot(self, snapshot: Snapshot):
        super().restore_from_snapshot(snapshot)
        self.__integrity = snapshot.get_data(EntityDecaying, "integrity")

    #endregion

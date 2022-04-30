from __future__ import annotations
from typing import Type, Any, cast

from utils.action_queue import ActionPriorityQueue
import utils.activator as activator
from abc import ABCMeta

from zeroplayer.step_priorities import StepPriority
from zeroplayer.entities.entity import Entity


class EntityKillable(Entity, metaclass=ABCMeta):
    """An Entity that can be killed"""

    #region //// Init

    __killed: bool
    __no_residue: bool
    _residue_type: Type[Entity] | None = None
    _residue_params: tuple[Any, ...] = ()

    def __init__(self):
        self.__killed = False
        self.__no_residue = False
        super().__init__()

    #endregion

    #region //// Step

    def step(self, action_queue: ActionPriorityQueue) -> None:
        super().step(action_queue)
        action_queue.enqueue(StepPriority.KILL, self.__action_kill)

    def __action_kill(self):
        if not self.__killed: return
        self.kill_instant()

    #endregion

    #region //// Killing

    @property
    def is_killed(self):
        return self.__killed

    def kill(self, no_residue: bool = False):
        self.__killed = True
        self.__no_residue = self.__no_residue or no_residue

    def kill_instant(self):
        if self.location is None: return

        # Get residue spawn point
        residue_location = self.location
        residue_x = self.x
        residue_y = self.y

        # Remove self
        self.remove()

        # Spawn residue
        if self._residue_type is None: return
        if self.__no_residue: return

        residue = cast(Entity, activator.create_instance(self._residue_type, self._residue_params))
        residue.place_at(residue_location, residue_x, residue_y)

    #endregion

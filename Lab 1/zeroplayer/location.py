from __future__ import annotations
from utils.action_queue import ActionPriorityQueue

from zeroplayer.entity import Entity
from zeroplayer.spawn_rule import SpawnRule
from zeroplayer.step_priorities import StepPriority


class Location(Entity):
    """
    Represents a location.
    Can create new entities every step.

    Location may have "neighbours", which are stored
    in [id -> Location] dict.
    """

    def __init__(self):
        super().__init__()
        self.__init_neighbours()

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.SPAWN, self.__handle_spawn)
        super().step(queue)

    #region //// Spawning

    _rules: tuple[SpawnRule] = ()

    def __handle_spawn(self) -> None:
        for rule in self._rules:
            rule.spawn_as_child(self)

    #endregion

    #region //// Neighbours

    neighbours: dict[int, Location]

    def __init_neighbours(self):
        self.neighbours = dict()

    def add_neighbour(self, *args: Location) -> None:
        for location in args:
            self.neighbours[location.id] = location
            location.neighbours[self.id] = self

    def remove_neighbour(self, location: Location) -> None:
        self.neighbours.pop(location.id)
        location.neighbours.pop(self.id)

    #endregion

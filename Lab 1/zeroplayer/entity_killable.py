from __future__ import annotations
from typing import Optional
from entity import Entity
from spawn_rule import SpawnRule


class EntityKillable(Entity):

    _corpse_rules: tuple[SpawnRule] = ()

    # Only the last corpse entity will be used
    _transfer_children: bool = False
    _transfer_neighbours: bool = False

    __killed: bool

    def __init__(self):
        super().__init__()
        __killed = False

    def kill(self):
        self.__killed = True

    def end_step(self) -> None:
        super().end_step()
        if not self.__killed: return

        # Create corpses
        last_corpse: Optional[Entity] = None
        for rule in self.__class__._corpse_rules:
            last_corpse = rule.spawn_as_child(self.parent)

        # Transfer children
        if self._transfer_children:
            if not (last_corpse is None):
                last_corpse.add_children(*self.children)

        # Transfer neighbours
        if self._transfer_neighbours:
            if not (last_corpse is None):
                for neighbour in self.neighbours:
                    neighbour.add_neighbours(last_corpse)

        # Remove self
        if not (self.parent is None):
            self.parent.remove_child(self)

        for neighbour in self.neighbours:
            neighbour.remove_neighbour(self)

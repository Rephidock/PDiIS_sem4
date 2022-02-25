from __future__ import annotations
from typing import Optional
from entity import Entity
from spawn_rule import SpawnRule


class EntityKillable(Entity):

    _corpse_rules: tuple[SpawnRule] = ()
    _transfer_children: bool = False        # Only the last corpse entity will be used

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
                self.transfer_children(last_corpse)

        # Unlink self
        if not (self.parent is None):
            self.parent.remove_child(self)


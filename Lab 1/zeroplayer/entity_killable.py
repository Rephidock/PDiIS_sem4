from __future__ import annotations
from typing import Optional
from zeroplayer.entity import Entity
from zeroplayer.spawn_rule import SpawnRule


class EntityKillable(Entity):

    # Class variables
    _corpse_rules: tuple[SpawnRule] = ()
    _transfer_children: bool = False        # Only the last corpse entity will be used
    _max_lifetime: Optional[int] = None

    # Instance variables
    __killed: bool

    def __init__(self):
        super().__init__()
        __killed = False

    def kill(self):
        self.__killed = True

    def end_step(self) -> None:
        super().end_step()

        # Max lifetime
        if (self.__class__._max_lifetime is not None) and (self.lifetime >= self.__class__._max_lifetime):
            self.kill()

        # Guard
        if not self.__killed:
            return

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

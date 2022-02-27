from __future__ import annotations
from typing import Optional
from zeroplayer.entity_movable import EntityMovable
from zeroplayer.entity_killable import EntityKillable


class Creature(EntityKillable, EntityMovable):
    # Exists because max lifetime and MRO: First handle movement then killing

    _max_lifetime: Optional[int] = None

    def __init__(self):
        super().__init__()

    def end_step(self) -> None:
        # Max lifetime
        if (self.__class__._max_lifetime is not None) and (self.lifetime >= self.__class__._max_lifetime):
            self.kill()

        # Move, then kill
        super().end_step()

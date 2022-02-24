from __future__ import annotations
from typing import Optional, Type
from utils.randUtils import chance
from zeroplayer.entity import Entity


class SpawnRule:

    __entity_type: Type[Entity]
    __frequency: int
    __chance: float

    __call_counter: int

    def __init__(self, entitytype: Type[Entity], frequency: int = 1, chance_of_spawn: float = 1.0):
        self.__entity_type = entitytype
        self.__frequency = frequency
        self.__chance = chance_of_spawn

        self.__call_counter = 0

    def spawn(self) -> Optional[Entity]:
        self.__call_counter += 1
        if (self.__call_counter % self.__frequency != 0): return None   # Frequency check
        if not (chance(self.__chance)): return None                     # Chance check
        return self.__entity_type()

    def spawn_as_child(self, parent: Entity) -> None:
        child = self.spawn()
        if (child is None): return
        parent.add_children(child)

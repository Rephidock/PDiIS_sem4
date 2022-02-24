from __future__ import annotations
from typing import Type
from utils.randUtils import chance
from zeroplayer.entity import Entity


class SpawnRule:

    __entity_type: Type[Entity]
    __frequency: int
    __chance: float

    def __init__(self, entitytype: Type[Entity], frequency: int = 1, chance_of_spawn: float = 1.0):
        self.__entity_type = entitytype
        self.__frequency = frequency
        self.__chance = chance_of_spawn

    def spawn(self, parent: Entity) -> None:
        if (parent.lifetime % self.__frequency != 0): return
        if not (chance(self.__chance)): return
        parent.add_children(self.__entity_type())


class SpawnLocation(Entity):

    _rules: tuple[SpawnRule] = ()

    def begin_step(self) -> None:
        super().begin_step()
        for rule in self.__class__._rules:
            rule.spawn(self)

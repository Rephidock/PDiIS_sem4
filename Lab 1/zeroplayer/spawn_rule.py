from __future__ import annotations
from typing import Optional, Type, Any
from utils.rand_ext import chance
import utils.activator as activator
from zeroplayer.entities.entity import Entity


class SpawnRule:
    """
    A rule by which entities are created.
    """

    __entity_type: Type[Entity]
    __entity_args: tuple[Any]
    __period: int
    __chance: float

    __call_counter: int

    def __init__(self,
                 entity_type: Type[Entity],
                 entity_args: tuple[Any] = (),
                 period: int = 1,
                 chance_of_spawn: float = 1.0
                 ):
        self.__entity_type = entity_type
        self.__entity_args = entity_args
        self.__period = period
        self.__chance = chance_of_spawn

        self.__call_counter = 0

        if self.__period < 1:
            raise ArithmeticError("Spawn period must be at least 1 step (equivalent of every step)")

    def spawn(self) -> Optional[Entity]:
        self.__call_counter += 1

        # Frequency check
        if self.__call_counter % self.__period != 0:
            return None

        # Chance check
        if not (chance(self.__chance)):
            return None

        return activator.create_instance(self.__entity_type, self.__entity_args)

    def spawn_as_child(self, parent: Optional[Entity]) -> Optional[Entity]:
        child = self.spawn()

        # None guards
        if child is None:
            return None
        if parent is None:
            return child

        parent.add_children(child)
        return child

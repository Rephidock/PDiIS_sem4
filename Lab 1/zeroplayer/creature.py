from __future__ import annotations
from typing import Optional
from zeroplayer.entity_movable import EntityMovable
from zeroplayer.entity_killable import EntityKillable


class Creature(EntityKillable, EntityMovable):

    # Class variables
    _max_lifetime: Optional[int] = None
    _starting_satiety: float = 0.8
    _hunger_rate: float = 0.1
    _eating_threshold: float = 0.4  # 0.0 - 1.0

    # Instance variables
    _satiety: float  # 0.0-1.0

    def __init__(self):
        super().__init__()
        self._satiety = self.__class__._starting_satiety

    def eat(self) -> None:
        pass

    def begin_step(self) -> None:
        # Hunger
        self._satiety -= self.__class__._hunger_rate

        # Eating
        if self._satiety <= self.__class__._eating_threshold:
            self.eat()

    def end_step(self) -> None:
        # Max lifetime
        if (self.__class__._max_lifetime is not None) and (self.lifetime >= self.__class__._max_lifetime):
            self.kill()

        # Starvation
        if self._satiety <= 0:
            self.kill()

        # Note MRO: Move, then kill
        super().end_step()

from __future__ import annotations
from zeroplayer.entity_killable import EntityKillable


class Resource(EntityKillable):

    # Class
    _threshold: float = 0
    _decay: float = 0

    # Instance
    _value: float

    def __init__(self, initial_value: float):
        super().__init__()
        self._value = initial_value

    def take(self, value: float) -> None:
        self._value -= value

    def begin_step(self) -> None:
        super().begin_step()
        self._value -= self.__class__._decay

    def end_step(self) -> None:
        # Check resource value
        if self._value <= self.__class__._threshold:
            self.kill()

        # Move, then kill
        super().end_step()

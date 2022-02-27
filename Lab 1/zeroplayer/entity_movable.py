from __future__ import annotations
from typing import Optional
from zeroplayer.entity import Entity


class EntityMovable(Entity):

    __move_target: Optional[Entity]

    def __init__(self):
        super().__init__()
        self.__move_target = None

    def move(self, target: Optional[Entity]):
        self.__move_target = target

    def end_step(self) -> None:
        super().end_step()
        if self.__move_target is None: return

        self.replace_parent(self.__move_target)

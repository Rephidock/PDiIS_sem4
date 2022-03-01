from __future__ import annotations
import utils.rand_ext as rand_ext
from zeroplayer.entity import Entity


class EntityMovable(Entity):
    """
    An entity that can move or be moved.
    If during a step multiple moves need to be performed,
    a random one is selected.
    """

    __move_target: list[Entity]

    def __init__(self):
        super().__init__()
        self.__move_target = list()

    def move(self, target: Entity):
        self.__move_target.append(target)

    def end_step(self) -> None:
        super().end_step()

        # No movement
        if len(self.__move_target) < 1:
            return

        # Pick move target at random
        self.replace_parent(rand_ext.list_pick_random(self.__move_target))

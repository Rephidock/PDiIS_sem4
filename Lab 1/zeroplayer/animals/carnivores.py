from __future__ import annotations
from typing import Type, TYPE_CHECKING, Generator

from zeroplayer.entities.entity_creature import EntityCreature

from zeroplayer.animals import herbivores

# annotations
if TYPE_CHECKING:
    from zeroplayer.entities.entity_killable import EntityKillable


class Fox(EntityCreature):

    _max_lifetime: int = 30

    _residue_type = None

    _prey_types: tuple[EntityKillable, ...] = (herbivores.Rabbit, herbivores.DeadRabbit)
    _satiety_multipliers: dict[Type[EntityKillable], float] = {
        herbivores.Rabbit: 0.9,
        herbivores.DeadRabbit: 0.8
    }

    _procreation_chance: float = 0.5  # 0 <= value <= 1
    _procreation_cooldown: int = 5

    # Movement and vision
    _vision_distance = 6
    _shift_distance = 2

    @classmethod
    def get_allowed_shifts(cls) -> Generator[tuple[int, int], None, None]:
        for xx in range(-cls._shift_distance, cls._shift_distance+1):
            for yy in range(-cls._shift_distance, cls._shift_distance+1):
                yield xx, yy


class Owl(EntityCreature):

    _max_lifetime: int = 30

    _residue_type = None

    _prey_types: tuple[EntityKillable, ...] = (herbivores.Mouse, herbivores.DeadMouse)
    _satiety_multipliers: dict[Type[EntityKillable], float] = {
        herbivores.Mouse: 0.9,
        herbivores.DeadMouse: 0.8
    }

    _procreation_chance: float = 0.5  # 0 <= value <= 1
    _procreation_cooldown: int = 5

    # Movement and vision
    _vision_distance = 8
    _shift_distance = 2

    @classmethod
    def get_allowed_shifts(cls) -> Generator[tuple[int, int], None, None]:
        for xx in range(-cls._shift_distance, cls._shift_distance + 1):
            for yy in range(-cls._shift_distance, cls._shift_distance + 1):
                yield xx, yy

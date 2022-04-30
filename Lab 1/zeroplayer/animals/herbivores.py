from __future__ import annotations
from typing import Type, TYPE_CHECKING

from zeroplayer.entities.entity_decaying import EntityDecaying
from zeroplayer.entities.entity_creature import EntityCreature

from zeroplayer.animals import plants

# annotations
if TYPE_CHECKING:
    from zeroplayer.entities.entity_killable import EntityKillable


class DeadRabbit(EntityDecaying):

    _integrity_cap: float = 1.0
    _integrity_start: float = 1.0
    _decay_speed: float = 0.2


class DeadMouse(EntityDecaying):

    _integrity_cap: float = 1.0
    _integrity_start: float = 1.0
    _decay_speed: float = 0.25


class Rabbit(EntityCreature):

    _max_lifetime: int = 30

    _residue_type = DeadRabbit
    _residue_params = ()

    _prey_types: tuple[EntityKillable, ...] = (plants.Grass,)
    _satiety_multipliers: dict[Type[EntityKillable], float] = {
        plants.Grass: 0.85
    }

    _procreation_chance: float = 0.5  # 0 <= value <= 1
    _procreation_cooldown: int = 2


class Mouse(EntityCreature):

    _max_lifetime: int = 15

    _residue_type = DeadMouse
    _residue_params = ()

    _prey_types: tuple[EntityKillable, ...] = (plants.Grass, plants.Wheat)
    _satiety_multipliers: dict[Type[EntityKillable], float] = {
        plants.Grass: 0.6,
        plants.Wheat: 0.8
    }

    _procreation_chance: float = 0.8  # 0 <= value <= 1
    _procreation_cooldown: int = 3

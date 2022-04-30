from zeroplayer.entities.entity_decaying import EntityDecaying


class Grass(EntityDecaying):

    _integrity_cap: float = 1.0
    _integrity_start: float = 1.0
    _decay_speed: float = 0.05


class Wheat(EntityDecaying):

    _integrity_cap: float = 1.0
    _integrity_start: float = 0.8
    _decay_speed: float = 0.1

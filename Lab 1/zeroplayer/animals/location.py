from zeroplayer.location import Location, SpawnRule
from zeroplayer.animals import plants
from zeroplayer.animals import herbivores
from zeroplayer.animals import carnivores


class WoodlandEdge(Location):

    _spawn_rules: tuple[SpawnRule, ...] = (
        SpawnRule(plants.Grass, (), 0, 6, 0.75),
        SpawnRule(plants.Wheat, (), 0, 3, 0.75),
        SpawnRule(herbivores.Mouse, (), 1, 1, 0.25),
        SpawnRule(herbivores.Rabbit, (), 1, 1, 0.2),
        SpawnRule(carnivores.Owl, (), 1, 1, 0.1),
        SpawnRule(carnivores.Fox, (), 1, 1, 0.1)
    )

    _width = 20
    _height = 10
    _initial_rolls = 10

    def __init__(self, create_empty: bool = False):
        super().__init__(
            self._width,
            self._initial_rolls,
            self._spawn_rules, 0 if create_empty else self._initial_rolls
        )

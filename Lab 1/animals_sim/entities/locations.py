from zeroplayer.entities.location import Location
from zeroplayer.spawn_rule import SpawnRule

import animals_sim.entities.plants as plants


class Forest(Location):
    _rules = (
        SpawnRule(plants.Grass, (2,), chance_of_spawn=0.3),
        SpawnRule(plants.Grass, (8,), chance_of_spawn=0.2, period=3),
    )


class Field(Location):
    _rules = (
        SpawnRule(plants.Wheat, (10,), chance_of_spawn=0.7, period=8),
        SpawnRule(plants.Wheat, (8,), chance_of_spawn=0.4, period=2),
        SpawnRule(plants.Wheat, (4,), chance_of_spawn=0.2),
        SpawnRule(plants.Grass, (2,), chance_of_spawn=0.2)
    )

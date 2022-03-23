from zeroplayer.entities.creature import Creature, IntakeRule
from zeroplayer.entities.resource import Resource
from zeroplayer.entities.location import Location
from zeroplayer.spawn_rule import SpawnRule
from random import choice
from typing import cast

import animals_sim.entities.plants as plants


class Mouse(Creature):
    _max_lifetime = 15

    _satiety_hunger_rate = 0.2

    _intake_rules = {
        plants.Wheat: IntakeRule(value_mult=0.2, request_starved=8, request_stuffed=0.8, request_weight=3),
        plants.Grass: IntakeRule(value_mult=0.2, request_starved=6, request_stuffed=0.8, request_weight=1)
    }

    _procreation_spawn_count = 3
    _procreation_male_threshold = 1

    def _intake(self):
        searched = self._search_food()
        if not bool(searched):
            location_neighbours = list(cast(Location, self.parent).neighbours.values())
            self.move(choice(location_neighbours))
        else:
            self._request_food(searched)

    @classmethod
    def set_spawn_rules(cls):
        cls._procreation_spawn_rules = (SpawnRule(cls, chance_of_spawn=0.4),)
        cls._residue_rules = (SpawnRule(MouseMeat, (1,)),)


class MouseMeat(Resource):
    _decay_speed_start = 0.1
    _decay_acceleration = 0.1


class Rabbit(Creature):
    _max_lifetime = 20

    _intake_rules = {
        plants.Grass: IntakeRule(value_mult=0.2, request_starved=8, request_stuffed=0.8, request_weight=1)
    }

    _procreation_spawn_count = 2
    _procreation_male_threshold = 1

    def _intake(self):
        searched = self._search_food()
        if not bool(searched):
            location_neighbours = list(cast(Location, self.parent).neighbours.values())
            self.move(choice(location_neighbours))
        else:
            self._request_food(searched)

    @classmethod
    def set_spawn_rules(cls):
        cls._procreation_spawn_rules = (SpawnRule(cls, chance_of_spawn=0.5),)
        cls._residue_rules = (SpawnRule(RabbitMeat, (1,)),)


class RabbitMeat(Resource):
    _decay_speed_start = 0.1
    _decay_acceleration = 0.1


# Because class cannot be referenced during its definition
Mouse.set_spawn_rules()
Rabbit.set_spawn_rules()

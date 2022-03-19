from zeroplayer.entities.creature import Creature, IntakeRule
from zeroplayer.entities.location import Location
from zeroplayer.spawn_rule import SpawnRule
from random import choice
from typing import cast

import animals_sim.entities.herbivores as herbivores


class Owl(Creature):
    _max_lifetime = 50

    _satiety_hunger_rate = 0.2

    _intake_rules = {
        herbivores.MouseMeat: IntakeRule(value_mult=0.3, request_starved=3, request_stuffed=0.5),
    }

    def _intake(self):
        found_food = self._search_food()
        found_food_is_empty = not bool(found_food)
        found_targets = self.parent.children_by_type(herbivores.Mouse)
        found_targets_is_empty = not bool(found_targets)
        # is_nearly_starved = self.satiety < 0.2

        if found_food_is_empty and found_targets_is_empty:
            location_neighbours = list(cast(Location, self.parent).neighbours.values())
            self.move(choice(location_neighbours))
        elif found_food_is_empty:
            cast(Creature, choice(found_targets)).kill()
        else:
            self._request_food(found_food)

    _procreation_spawn_count = 1
    _procreation_male_threshold = 1

    @classmethod
    def set_spawn_rules(cls):
        cls._procreation_spawn_rules = (SpawnRule(cls, chance_of_spawn=0.5),)


class Fox(Creature):
    _max_lifetime = 50

    _satiety_hunger_rate = 0.2

    _intake_rules = {
        herbivores.RabbitMeat: IntakeRule(value_mult=0.3, request_starved=2, request_stuffed=0.5),
    }

    def _intake(self):
        found_food = self._search_food()
        found_food_is_empty = not bool(found_food)
        found_targets = self.parent.children_by_type(herbivores.Mouse)
        found_targets_is_empty = not bool(found_targets)
        # is_nearly_starved = self.satiety < 0.2

        if found_food_is_empty and found_targets_is_empty:
            location_neighbours = list(cast(Location, self.parent).neighbours.values())
            self.move(choice(location_neighbours))
        elif found_food_is_empty:
            cast(Creature, choice(found_targets)).kill()
        else:
            self._request_food(found_food)

    _procreation_spawn_count = 1
    _procreation_male_threshold = 1

    @classmethod
    def set_spawn_rules(cls):
        cls._procreation_spawn_rules = (SpawnRule(cls, chance_of_spawn=0.5),)


Owl.set_spawn_rules()
Fox.set_spawn_rules()

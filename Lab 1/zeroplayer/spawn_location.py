from __future__ import annotations
from zeroplayer.entity import Entity
from zeroplayer.spawn_rule import SpawnRule


class SpawnLocation(Entity):
    """
    An entity that creates new entities via spawn rules.
    Can create new entities every step.
    """

    _rules: tuple[SpawnRule] = ()

    def begin_step(self) -> None:
        super().begin_step()
        for rule in self.__class__._rules:
            rule.spawn_as_child(self)

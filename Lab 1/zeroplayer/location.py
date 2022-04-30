from __future__ import annotations
from typing import TYPE_CHECKING, Type, Any, Generator

from abc import ABCMeta
from dataclasses import dataclass
from random import randint
from math import floor

from utils.rand_ext import chance
import utils.activator as activator
from utils.action_queue import ActionPriorityQueue
from utils.math import clamp

from zeroplayer.snapshotable import Snapshotable, Snapshot

# annotations
if TYPE_CHECKING:
    from zeroplayer.entities.entity import Entity


class Location(Snapshotable, metaclass=ABCMeta):
    """
    The grid of the simulation.
    Stores all entities, gets and performs step actions.
    """

    #region //// Init

    def __init__(self, width: int, height: int, spawn_rules: tuple[SpawnRule, ...] = (), initial_spawn_rolls: int = 0):
        # Field
        self.__width = width
        self.__height = height
        self.clear()

        # Spawning
        self.__spawn_rules = spawn_rules
        self.spawning_enabled = True
        for _ in range(initial_spawn_rolls):
            self.spawn()

        # Stepping
        self.__actions = ActionPriorityQueue()

    #endregion

    #region //// Field

    __width: int
    __height: int
    rows: list[list[Entity | None]]  # List of rows

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def clear(self):
        """Creates a new empty field"""
        self.rows = [[None for _ in range(self.__width)] for _ in range(self.__height)]

    def clamp_position(self, x: int, y: int) -> tuple[int, int]:
        """Returns position clamped to within location"""
        return round(clamp(x, 0, self.__width-1)), round(clamp(y, 0, self.__height-1))

    def entity_at_position(self, x: int, y: int) -> Entity | None:
        """Returns entity as position on the field"""
        x, y = self.clamp_position(x, y)
        return self[x, y]

    def position_empty(self, x: int, y: int) -> bool:
        return self.entity_at_position(x, y) is None

    def __getitem__(self, key: tuple[int, int]):
        return self.rows[key[1]][key[0]]

    def __setitem__(self, key: tuple[int, int], value: Entity | None):
        self.rows[key[1]][key[0]] = value

    def __iter__(self) -> Generator[Entity | None, None, None]:
        """Iterates over all entities in reading order"""
        for row in self.rows:
            for entity in row:
                yield entity

    #endregion

    #region //// Stepping

    __actions: ActionPriorityQueue

    def step(self) -> None:
        """Gets and performs all actions among entities"""

        # Get actions
        for entity in self:
            if entity is not None:
                entity.step(self.__actions)

        # Spawn new entities
        self.spawn()

        # Perform actions
        self.__actions.perform()

    #endregion

    #region //// Spawning

    __spawn_rules: tuple[SpawnRule, ...] = ()
    spawning_enabled: bool

    def spawn(self):

        # Disabled guard
        if not self.spawning_enabled: return

        # Perform spawn rules
        for rule in self.__spawn_rules:

            # Chance
            if not chance(rule.spawn_chance): continue

            # Quantity
            spawns_count = \
                randint(rule.quantity_min, rule.quantity_max) \
                if rule.quantity_min < rule.quantity_max \
                else rule.quantity_min

            # Spawning
            for i in range(spawns_count):

                # Pick position
                x = randint(0, self.width-1)
                y = randint(0, self.height-1)

                # Spawn in unoccupied
                if self.entity_at_position(x, y) is None:
                    entity = activator.create_instance(rule.entity_type, rule.entity_params)
                    entity.place_at(self, x, y)

    #endregion

    #region //// Snapshot

    def fill_snapshot(self, snapshot: Snapshot):

        # Field
        snapshot.set_data(Location, "width", self.__width)
        snapshot.set_data(Location, "height", self.__height)

        # Entities
        def helper_process_entity(entity):
            if entity is None: return None

            entity_snapshot = entity.form_snapshot()
            entity_snapshot.set_data(None, "type", type(entity))
            return entity_snapshot

        field = [helper_process_entity(entity) for entity in self]
        snapshot.set_data(Location, "field", field)

        # Spawning
        snapshot.set_data(Location, "doSpawn", self.spawning_enabled)

    def restore_from_snapshot(self, snapshot: Snapshot):

        # Field
        self.__width = snapshot.get_data(Location, "width")
        self.__height = snapshot.get_data(Location, "height")
        self.clear()

        # Entities
        for i, entity_snapshot in enumerate(snapshot.get_data(Location, "field")):
            if entity_snapshot is None: continue

            entity = entity_snapshot.get_data(None, "type")()
            entity.place_at(self, i % self.width, floor(i / self.width))
            entity.restore_from_snapshot(entity_snapshot)

        # Spawning
        self.spawning_enabled = snapshot.get_data(Location, "doSpawn")

    #endregion


@dataclass
class SpawnRule:
    entity_type: Type[Entity]
    entity_params: tuple[Any, ...]
    quantity_min: int
    quantity_max: int
    spawn_chance: float

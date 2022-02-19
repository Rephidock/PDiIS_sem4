from __future__ import annotations
from typing import Callable, List
from queue import Queue


class Entity:

    id: int
    lifetime: int

    id = 0

    def __init__(self):
        self.init_changes()
        self.init_relations()

        self.id = Entity.id
        Entity.id += 1

        self.lifetime = 0

    def step(self) -> None:
        self.lifetime += 1

    #region //// Changes queue

    # During a step of simulation
    # no change should have impact on another entity
    # Thus a queue is used
    __changes: Queue[Callable[[Entity], None]]

    def init_changes(self):
        self.__changes = Queue()

    def enqueue_changes(self, *args: Callable[[Entity], None]) -> None:
        for arg in args:
            self.__changes.put(arg)

    def perform_changes(self) -> None:
        while not self.__changes.empty():
            self.__changes.get()(self)

    #endregion

    #region //// Parent-child-neighbour

    parents: List[Entity]
    children: List[Entity]
    neighbours: List[Entity]

    def init_relations(self):
        self.parents = list()
        self.children = list()
        self.neighbours = list()

    def add_parents(self, *args: Entity) -> None:
        for parent in args:
            self.parents.append(parent)
            parent.children.append(self)

    def add_children(self, *args: Entity) -> None:
        for child in args:
            self.children.append(child)
            child.parents.append(self)

    def add_neighbours(self, *args: Entity) -> None:
        for neighbour in args:
            self.neighbours.append(neighbour)
            neighbour.neighbours.append(self)

    #endregion

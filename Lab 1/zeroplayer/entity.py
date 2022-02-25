from __future__ import annotations
from typing import Optional


class Entity:

    id: int
    lifetime: int

    id = 0

    def __init__(self):
        self.init_parent_child()
        self.init_neighbour()

        self.id = Entity.id
        Entity.id += 1

        self.lifetime = 0

    #region //// Stepping

    def begin_step(self) -> None:
        self.lifetime += 1

    def step(self) -> None:
        pass

    def end_step(self) -> None:
        pass

    def begin_step_children(self) -> None:
        for child in self.children:
            child.begin_step()
            child.begin_step_children()

    def step_children(self) -> None:
        for child in self.children:
            child.step()
            child.step_children()

    def end_step_children(self) -> None:
        for child in self.children:
            child.end_step()
            child.end_step_children()

    #endregion

    #region //// Parent-child

    parent: Optional[Entity]
    children: list[Entity]

    def init_parent_child(self):
        self.parent = None
        self.children = list()

    def add_children(self, *args: Entity) -> None:
        for child in args:
            self.children.append(child)
            child.replace_parent(self)

    def replace_parent(self, new_parent: Optional[Entity]) -> None:
        if not (self.parent is None):
            self.parent.remove_child(self)
        if not (new_parent is None):
            new_parent.add_children(self)
        self.parent = new_parent

    def remove_child(self, child: Entity) -> None:
        self.children = list(filter(lambda entity, target_id=child.id: entity.id != target_id, self.children))
        child.parent = None

    #endregion

    #region //// Neighbour

    neighbours: list[Entity]

    def init_neighbour(self):
        self.neighbours = list()

    def add_neighbours(self, *args: Entity) -> None:
        for neighbour in args:
            self.neighbours.append(neighbour)
            neighbour.neighbours.append(self)

    def remove_neighbour(self, neighbour: Entity) -> None:
        self.neighbours = list(
            filter(lambda entity, target_id=neighbour.id: entity.id != target_id, self.neighbours)
        )
        neighbour.neighbours = list(
            filter(lambda entity, target_id=self.id: entity.id != target_id, neighbour.neighbours)
        )

    #endregion


class RootEntity(Entity):

    def root_step(self) -> None:
        self.begin_step()
        self.begin_step_children()
        self.step()
        self.step_children()
        self.end_step()
        self.end_step_children()

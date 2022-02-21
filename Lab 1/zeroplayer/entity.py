from __future__ import annotations


class Entity:

    id: int
    lifetime: int

    id = 0

    def __init__(self):
        self.init_relations()

        self.id = Entity.id
        Entity.id += 1

        self.lifetime = 0

    def step(self) -> None:
        self.lifetime += 1

    #region //// Parent-child-neighbour

    parents: list[Entity]
    children: list[Entity]
    neighbours: list[Entity]

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

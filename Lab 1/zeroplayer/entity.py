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

    #region //// Stepping

    def root_step(self) -> None:
        self.begin_step()
        self.begin_step_children()
        self.step()
        self.step_children()
        self.end_step()
        self.end_step_children()

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

from __future__ import annotations
from typing import Optional, Type


class Entity:

    id: int = 0

    lifetime: int

    def __init__(self):
        self.init_parent_child()

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

    #endregion

    #region //// Stepping children

    def begin_step_children(self) -> None:
        for child in self.children.values():
            child.begin_step()
            child.begin_step_children()

    def step_children(self) -> None:
        for child in self.children.values():
            child.step()
            child.step_children()

    def end_step_children(self) -> None:
        for child in self.children.values():
            child.end_step()
            child.end_step_children()

    #endregion

    #region //// Parent-child

    parent: Optional[Entity]
    children: dict[int, Entity]

    def init_parent_child(self):
        self.parent = None
        self.children = dict()

    def add_children(self, *args: Entity) -> None:
        for child in args:
            self.children[child.id] = child
            child.replace_parent(self)

    def replace_parent(self, new_parent: Optional[Entity]) -> None:
        if not (self.parent is None):
            self.parent.remove_child(self)
        if not (new_parent is None):
            new_parent.add_children(self)
        self.parent = new_parent

    def remove_child(self, child: Entity) -> None:
        child = self.children.pop(child.id, None)
        if child is not None:
            child.parent = None

    def transfer_children(self, new_parent: Optional[Entity]) -> None:
        # Directly break parent link
        for child in self.children.values():
            child.parent = None

        # Directly break child link
        children = self.children
        self.children.clear()

        # Make new parent <-> child links
        new_parent.add_children(*children)

    def children_by_type(self, desired_class: Type[Entity]) -> list[Entity]:
        ret = list()
        for child in self.children.values():
            if issubclass(desired_class, child.__class__):
                ret.append(child)
        return ret

    #endregion


class RootEntity(Entity):

    def root_step(self) -> None:
        self.begin_step()
        self.begin_step_children()
        self.step()
        self.step_children()
        self.end_step()
        self.end_step_children()

from __future__ import annotations
from typing import Optional, Type, Any
from zeroplayer.action_queue import StepPriority, ActionPriorityQueue


class Entity:
    """
    Base class for all things in a zero player step simulation.

    Each entity has
      - a (sequential) numeric id
      - lifetime counter
      - optional parent reference
      - children, stored in an [id -> Entity] dict
      - step event (see also: steps.md)

    When inheriting, extend the step method instead of simple override:
    Perform super().step(queue) calls at the end.
    """

    __pending_id: int = 0

    __id: int
    __lifetime: int

    def __init__(self):
        self.__init_parent_child()

        self.__id = Entity.__pending_id
        Entity.__pending_id += 1

        self.__lifetime = 0

    #region //// Properties

    @property
    def id(self) -> int:
        return self.__id

    @property
    def lifetime(self) -> int:
        return self.__lifetime

    #endregion

    #region //// Stepping

    def __handle_lifetime(self) -> None:
        self.__lifetime += 1

    def step(self, queue: ActionPriorityQueue) -> None:
        # Self
        queue.enqueue(StepPriority.LIFETIME, self, self.__handle_lifetime)

        # Children
        for child in self.children.values():
            child.step(queue)

    #endregion

    #region //// Parent-child

    # The link is always 2-way

    parent: Optional[Entity]
    children: dict[int, Entity]

    def __init_parent_child(self):
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

    def children_by_type(self, desired_class: Type[Entity]) -> list[Any]:
        """Returns a list with all children which are a subclass of the given"""

        ret = list()
        for child in self.children.values():
            if issubclass(desired_class, child.__class__):
                ret.append(child)
        return ret

    #endregion


class RootEntity(Entity):
    """
    The root of the zero player simulation.
    Begins the step call chain.
    Stores and performs actions.
    """

    __actions: ActionPriorityQueue

    def __init__(self):
        super().__init__()
        self.__actions = ActionPriorityQueue()

    def root_step(self) -> None:

        # Get actions
        self.step(self.__actions)

        # Perform actions
        self.__actions.perform()

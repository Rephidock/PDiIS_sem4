from typing import Optional
from zeroplayer.entity import Entity
from zeroplayer.action_queue import StepPriority, ActionPriorityQueue
from zeroplayer.spawn_rule import SpawnRule


class EntityKillable(Entity):
    """
    An entity that can be killed or destroyed.
    When this entity is destroyed it may
    create residue entities (new entities) in its place.
    """

    # Class variables
    _residue_rules: tuple[SpawnRule] = ()
    _transfer_children: bool = False        # Only the last residue entity will be used

    # Instance variables
    __killed: bool

    def __init__(self):
        super().__init__()
        self.__killed = False

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.KILL, self, self.__handle_death)
        super().step(queue)

    def kill(self):
        self.__killed = True

    def __handle_death(self) -> None:

        # Guard
        if not self.__killed:
            return

        # Create corpses
        last_residue: Optional[Entity] = None
        for rule in self.__class__._residue_rules:
            last_residue = rule.spawn_as_child(self.parent)

        # Transfer children
        if self._transfer_children:
            if not (last_residue is None):
                self.transfer_children(last_residue)

        # Unlink self
        if not (self.parent is None):
            self.parent.remove_child(self)

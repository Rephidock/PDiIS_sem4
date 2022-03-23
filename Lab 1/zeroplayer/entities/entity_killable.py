from typing import Optional
from utils.action_queue import ActionPriorityQueue
from zeroplayer.entities.entity import Entity
from zeroplayer.step_priorities import StepPriority
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
        queue.enqueue(StepPriority.KILL, self.__handle_death)
        super().step(queue)

    def kill(self):
        self.__killed = True

    def __handle_death(self) -> None:

        # Guard
        if not self.__killed:
            return

        # Create residue
        last_residue: Optional[Entity] = None
        for rule in self._residue_rules:
            last_residue = rule.spawn_as_child(self.parent)

        # Transfer children
        if self._transfer_children:
            if last_residue is not None:
                self.transfer_children(last_residue)

        # Unlink self
        if self.parent is not None:
            self.parent.remove_child(self)

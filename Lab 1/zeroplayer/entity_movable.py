from utils.action_queue import ActionPriorityQueue
from random import choice
from zeroplayer.entity import Entity
from zeroplayer.step_priorities import StepPriority


class EntityMovable(Entity):
    """
    An entity that can move or be moved.
    If during a step multiple moves need to be performed,
    a random one is selected.
    """

    __move_target: list[Entity]

    def __init__(self):
        super().__init__()
        self.__move_target = list()

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.KILL, self.__handle_movement)
        super().step(queue)

    def move(self, target: Entity):
        self.__move_target.append(target)

    def __handle_movement(self) -> None:

        # No movement
        if len(self.__move_target) < 1:
            return

        # Pick move target at random
        self.replace_parent(choice(self.__move_target))

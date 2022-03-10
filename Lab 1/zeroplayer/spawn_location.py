from utils.action_queue import ActionPriorityQueue

from zeroplayer.entity import Entity
from zeroplayer.spawn_rule import SpawnRule
from zeroplayer.step_priorities import StepPriority


class SpawnLocation(Entity):
    """
    An entity that creates new entities via spawn rules.
    Can create new entities every step.
    """

    _rules: tuple[SpawnRule] = ()

    def step(self, queue: ActionPriorityQueue) -> None:
        queue.enqueue(StepPriority.SPAWN, self, self.__handle_spawn)
        super().step(queue)

    def __handle_spawn(self) -> None:
        for rule in self._rules:
            rule.spawn_as_child(self)

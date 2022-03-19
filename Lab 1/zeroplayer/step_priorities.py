from utils.action_queue import ActionPriority


class StepPriority(ActionPriority):

    # Lower value - higher priority

    PRE = 0
    LIFETIME = 1
    SPAWN = 2

    BEGIN = 10
    HUNGER = 15
    DISTRIBUTE = 17

    NORMAL = 20

    END = 30
    DECAY = 31
    MOVE = 32
    EXHAUSTION = 33
    KILL = 35

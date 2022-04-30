from utils.action_queue import ActionPriority


class StepPriority(ActionPriority):

    # Lower value - higher priority

    LIFETIME = 5

    SEARCH = 6
    LEAP_ATTACK = 7
    WANDER = 8
    MOVE = 10

    AGE = 12
    DECAY = 13

    KILL = 15

    LEAP_MOVE = 18

    PROCREATION = 20

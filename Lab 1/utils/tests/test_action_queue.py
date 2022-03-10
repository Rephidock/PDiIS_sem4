import unittest
from utils.action_queue import ActionPriority, ActionPriorityQueue


class TestActionPriorityQueue(unittest.TestCase):

    class Priorities(ActionPriority):
        FIRST = 1
        SECOND = 2
        THIRD = 3

    class Performer:

        value: int

        def __init__(self):
            self.value = 0

        def set3(self):
            self.value = 3

        def mult4(self):
            self.value *= 4

        def add1(self):
            self.value += 1

    def test_queue(self):
        # Create queue and performer
        queue = ActionPriorityQueue()
        p = self.Performer()

        queue.enqueue(self.Priorities.FIRST, p.set3)
        queue.enqueue(self.Priorities.THIRD, p.mult4)
        queue.enqueue(self.Priorities.SECOND, p.add1)
        queue.perform()
        self.assertEqual(p.value, (3 + 1) * 4)

        queue.enqueue(self.Priorities.SECOND, p.add1)
        queue.enqueue(self.Priorities.FIRST, p.set3)
        queue.enqueue(self.Priorities.THIRD, p.mult4)
        queue.perform()
        self.assertEqual(p.value, (3 + 1) * 4)

        queue.enqueue(self.Priorities.THIRD, p.mult4)
        queue.enqueue(self.Priorities.SECOND, p.add1)
        queue.enqueue(self.Priorities.FIRST, p.set3)
        queue.perform()
        self.assertEqual(p.value, (3 + 1) * 4)


if __name__ == '__main__':
    unittest.main()

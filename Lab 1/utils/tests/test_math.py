import unittest
import utils.math as umath


class Tests(unittest.TestCase):

    def test_lerp(self):
        # Boundaries
        self.assertEqual(umath.lerp(4, 5, 0), 4)
        self.assertEqual(umath.lerp(4, 5, 1), 5)

        # Middle
        self.assertEqual(umath.lerp(4, 5, 0.5), 4.5)
        self.assertEqual(umath.lerp(4, 6, 0.5), 5)
        self.assertEqual(umath.lerp(1, 3, 0.25), 1.5)

        # Out of bounds
        self.assertEqual(umath.lerp(4, 5, 2), 6)
        self.assertEqual(umath.lerp(4, 5, -1), 3)

    def test_lerp_clamped(self):
        # Boundaries
        self.assertEqual(umath.lerp_clamped(4, 5, 0), 4)
        self.assertEqual(umath.lerp_clamped(4, 5, 1), 5)

        # Middle
        self.assertEqual(umath.lerp_clamped(4, 5, 0.5), 4.5)
        self.assertEqual(umath.lerp_clamped(4, 6, 0.5), 5)
        self.assertEqual(umath.lerp_clamped(1, 3, 0.25), 1.5)

        # Out of bounds
        self.assertEqual(umath.lerp_clamped(4, 5, 2), 5)
        self.assertEqual(umath.lerp_clamped(4, 5, -1), 4)

    def test_clamp(self):
        self.assertEqual(umath.clamp(0, 1, 2), 1)
        self.assertEqual(umath.clamp(1, 1, 2), 1)
        self.assertEqual(umath.clamp(2, 1, 2), 2)
        self.assertEqual(umath.clamp(3, 1, 2), 2)
        self.assertEqual(umath.clamp(1.5, 1, 2), 1.5)
        self.assertEqual(umath.clamp(1.3, 1, 2), 1.3)


if __name__ == '__main__':
    unittest.main()

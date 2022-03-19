import unittest
import utils.activator as activator


class TestActivator(unittest.TestCase):

    #region //// Classes

    class Dummy0:

        def __init__(self, *args):
            if len(args) > 0:
                raise AssertionError()

    class Dummy1:

        def __init__(self, arg0, *args):
            if len(args) > 0:
                raise AssertionError()

            self.arg0 = arg0

    class Dummy2:

        def __init__(self, arg0, arg1, *args):
            if len(args) > 0:
                raise AssertionError()

            self.arg0 = arg0
            self.arg1 = arg1

    class DummyVariable:

        def __init__(self, *args):
            self.args = args

    #endregion

    def test_activator(self):
        activator.create_instance(self.Dummy0, ())
        self.assertEqual(23, activator.create_instance(self.Dummy1, (23,)).arg0)
        self.assertEqual(5,  activator.create_instance(self.Dummy2, (7, 5)).arg1)
        self.assertEqual((8, 7), activator.create_instance(self.DummyVariable, (8, 7)).args)
        self.assertEqual((8, 7, -1), activator.create_instance(self.DummyVariable, (8, 7, -1)).args)


if __name__ == '__main__':
    unittest.main()

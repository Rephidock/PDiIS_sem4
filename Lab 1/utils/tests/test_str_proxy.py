from typing import Type, Callable, Any
import unittest
from utils.str_proxy import str_proxy


class TestProxy(unittest.TestCase):

    #region //// Custom classes

    class Dummy:
        name: str

        def __init__(self, name: str):
            self.name = name

        def __str__(self):
            return "Some Dummy over there"

    class DummyInheritedEmpty(Dummy):
        pass

    class DummyInherited(Dummy):
        hp: float

        def __init__(self, name: str, hp: float):
            super().__init__(name)
            self.hp = hp

    class Fruit:
        type: str

        def __init__(self, type_: str):
            self.type = type_

        def __str__(self):
            return f"{self.type} fruit"

    #endregion

    def test_str_proxy(self):

        overrides: dict[Type, Callable[[Any], str]] = {
            str: lambda obj: f"Str(\"{obj}\")",
            self.Dummy: lambda obj: f"{obj.name} the dummy",
            self.DummyInheritedEmpty: lambda obj: f"{obj.name} the empty inherited dummy"
        }

        # Absent (builtin)
        self.assertEqual(str_proxy(42, overrides), "42")

        # Present (builtin)
        self.assertNotEqual(str_proxy("Yolo", overrides), "Yolo")
        self.assertEqual(str_proxy("Yolo", overrides), "Str(\"Yolo\")")

        # Present (class)
        self.assertEqual(str_proxy(self.Dummy("Kin"), overrides), "Kin the dummy")
        self.assertEqual(str_proxy(self.DummyInheritedEmpty("Jake"), overrides), "Jake the empty inherited dummy")

        # Absent (class)
        lee = self.DummyInherited("Lee", 25)
        papaya = self.Fruit("Papaya")
        self.assertEqual(str_proxy(papaya, overrides), str(papaya))
        self.assertEqual(str_proxy(lee, overrides), str(lee))


if __name__ == '__main__':
    unittest.main()

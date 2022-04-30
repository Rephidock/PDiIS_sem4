from typing import Type, Callable, Any
import unittest
from utils.string_utils import str_proxy, str_replace_at


class TestStrings(unittest.TestCase):

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

    def test_replace_at(self):

        base_string = "abcdeABCDE"

        # Single characters
        self.assertEqual(str_replace_at(base_string, 0, "A"), "AbcdeABCDE")
        self.assertEqual(str_replace_at(base_string, 1, "0"), "a0cdeABCDE")
        self.assertEqual(str_replace_at(base_string, 5, "Q"), "abcdeQBCDE")
        self.assertEqual(str_replace_at(base_string, 9, "z"), "abcdeABCDz")

        # Longer strings
        self.assertEqual(str_replace_at(base_string, 0, "ABXY"), "ABXYeABCDE")
        self.assertEqual(str_replace_at(base_string, 1, "01"), "a01deABCDE")
        self.assertEqual(str_replace_at(base_string, 5, "QwEr"), "abcdeQwErE")
        self.assertEqual(str_replace_at(base_string, 7, "ZUL"), "abcdeABZUL")


if __name__ == '__main__':
    unittest.main()

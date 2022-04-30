from typing import Callable, Any
from dataclasses import dataclass
from enum import IntEnum

from utils.string_utils import str_proxy

from zeroplayer.location import Location
from zeroplayer.entities.entity_decaying import EntityDecaying
from zeroplayer.animals import plants, herbivores, carnivores


#region //// Colors

class Colors(IntEnum):
    DEFAULT = 39
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    LT_GRAY = 37
    DK_GRAY = 90
    LT_RED = 91
    LT_GREEN = 92
    LT_YELLOW = 93
    LT_BLUE = 94
    LT_MAGENTA = 95
    LT_CYAN = 96
    WHITE = 97


def colored(text: str, color_index: int | Colors) -> str:
    return f"\x1b[{int(color_index)}m{text}\x1b[{int(Colors.DEFAULT)}m"

#endregion


#region //// Colored proxy overrides

@dataclass
class ColorRule:
    range_bottom: float = float("-inf")
    color: Colors = Colors.DEFAULT


resource_color_rules: list[ColorRule] = [
    ColorRule(0.65, Colors.LT_GREEN),
    ColorRule(0.30, Colors.GREEN),
    ColorRule(0.00, Colors.DK_GRAY)
]


herbivores_color_rules: list[ColorRule] = [
    ColorRule(0.75, Colors.LT_BLUE),
    ColorRule(0.50, Colors.LT_CYAN),
    ColorRule(0.25, Colors.CYAN),
    ColorRule(0.00, Colors.DK_GRAY)
]


carnivores_color_rules: list[ColorRule] = [
    ColorRule(0.75, Colors.LT_MAGENTA),
    ColorRule(0.50, Colors.MAGENTA),
    ColorRule(0.25, Colors.RED),
    ColorRule(0.00, Colors.DK_GRAY)
]


def decaying_to_string(symbol: str, entity: EntityDecaying, color_rules: list[ColorRule]) -> str:
    picked_rule: ColorRule = ColorRule()
    for rule in color_rules:
        if entity.integrity >= rule.range_bottom:
            picked_rule = rule
            break

    return colored(symbol, picked_rule.color)


overrides_colored: dict[type, Callable[[Any], str]] = {
    # None
    type(None): lambda obj: colored("·", Colors.DK_GRAY),
    plants.Grass: lambda obj: decaying_to_string("g", obj, resource_color_rules),
    plants.Wheat: lambda obj: decaying_to_string("w", obj, resource_color_rules),
    herbivores.DeadMouse: lambda obj: decaying_to_string("m", obj, resource_color_rules),
    herbivores.DeadRabbit: lambda obj: decaying_to_string("r", obj, resource_color_rules),
    herbivores.Mouse: lambda obj: decaying_to_string("M", obj, herbivores_color_rules),
    herbivores.Rabbit: lambda obj: decaying_to_string("R", obj, herbivores_color_rules),
    carnivores.Fox: lambda obj: decaying_to_string("F", obj, carnivores_color_rules),
    carnivores.Owl: lambda obj: decaying_to_string("O", obj, carnivores_color_rules)
}

#endregion


#region //// Uncolored proxy overrides

overrides_uncolored: dict[type, Callable[[Any], str]] = {
    # None
    type(None): lambda obj: "·",
    plants.Grass: lambda obj: "g",
    plants.Wheat: lambda obj: "w",
    herbivores.DeadMouse: lambda obj: "m",
    herbivores.DeadRabbit: lambda obj: "r",
    herbivores.Mouse: lambda obj: "M",
    herbivores.Rabbit: lambda obj: "R",
    carnivores.Fox: lambda obj: "F",
    carnivores.Owl: lambda obj: "O"
}

#endregion


#region //// Print Location

def print_location(location: Location, print_colored: bool):
    """Prints current location state with all entities"""

    proxy_overrides = overrides_colored if print_colored else overrides_uncolored

    for row in location.rows:
        for entity in row:
            print(str_proxy(entity, proxy_overrides), end="")
        print("\n", end="")

#endregion

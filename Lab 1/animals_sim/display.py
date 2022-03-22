from typing import Callable, Any
from zeroplayer.entities.entity import RootEntity
from zeroplayer.entities.resource import Resource
from zeroplayer.entities.creature import Creature, Gender
import animals_sim.entities as entities


# Display function
def creature_display(name: str, obj: Creature) -> str:
    gender_symbol = "♂" if obj.gender == Gender.MALE else "♀"
    return f"{name}[{gender_symbol} Age {obj.lifetime} Sat {obj.satiety:.2f}]"


def resource_display(name: str, obj: Resource) -> str:
    return f"{name}[{obj.value:.2f}]"


# Proxy overrides
overrides: dict[type, Callable[[Any], str]] = {

    # Root
    RootEntity: lambda obj: f"Simulation (step {obj.lifetime})",

    # Locations
    entities.locations.Forest: lambda obj: f"Forest ({obj.id})",
    entities.locations.Field: lambda obj: f"Field ({obj.id})",

    # Resources
    entities.plants.Wheat: lambda obj: resource_display("Wheat", obj),
    entities.plants.Grass: lambda obj: resource_display("Grass", obj),
    entities.herbivores.MouseMeat: lambda obj: resource_display("MouseMeat", obj),
    entities.herbivores.RabbitMeat: lambda obj: resource_display("RabbitMeat", obj),

    # Creatures
    entities.herbivores.Mouse: lambda obj: creature_display("Mouse", obj),
    entities.herbivores.Rabbit: lambda obj: creature_display("Rabbit", obj),
    entities.predators.Owl: lambda obj: creature_display("Owl", obj),
    entities.predators.Fox: lambda obj: creature_display("Fox", obj)
}

# Forced chunks
forced_chunks: list[type] = [
    entities.locations.Forest,
    entities.locations.Field
]

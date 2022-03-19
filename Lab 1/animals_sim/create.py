from zeroplayer.entities.entity import RootEntity
import animals_sim.entities as entities


def create_new() -> RootEntity:

    # Root
    ret = RootEntity()

    # Locations
    forest1 = entities.locations.Forest()
    forest2 = entities.locations.Forest()
    field = entities.locations.Field()

    forest1.add_neighbour(forest2, field)
    field.add_neighbour(forest2)

    ret.add_children(forest1, forest2, field)

    # Return
    return ret

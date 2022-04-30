from commands.base import SubcommandInfo, SubcommandName, DestName
import zeroplayer.animals as animal_sim


class SubcommandPlace(SubcommandInfo):

    @staticmethod
    def get_name():
        return SubcommandName.place

    @staticmethod
    def get_help():
        return "Places a new entity on the field"

    @staticmethod
    def form_parser(parser) -> None:
        parser.add_argument(
            DestName.place_x,
            action="store",
            help="x position (0-based, 0 is left most)",
            type=int
        )
        parser.add_argument(
            DestName.place_y,
            action="store",
            help="y position (0-based, 0 is top most)",
            type=int
        )
        parser.add_argument(
            DestName.place_type,
            action="store",
            help="entity type to spawn",
            choices=SubcommandPlace.dict_param_to_type.keys(),
        )

    dict_param_to_type: dict[str, type] = {
        "grass": animal_sim.plants.Grass,
        "wheat": animal_sim.plants.Wheat,
        "mouse": animal_sim.herbivores.Mouse,
        "rabbit": animal_sim.herbivores.Rabbit,
        "owl": animal_sim.carnivores.Owl,
        "fox": animal_sim.carnivores.Fox
    }

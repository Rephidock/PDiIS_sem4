from commands.base import SubcommandInfo, SubcommandName, DestName


class SubcommandNaturalSpawn(SubcommandInfo):

    @staticmethod
    def get_name():
        return SubcommandName.natural_spawn

    @staticmethod
    def get_help():
        return "Toggle natural spawning of new entities (except procreation)"

    @staticmethod
    def form_parser(parser) -> None:
        parser.add_argument(
            DestName.natural_lock,
            action="store",
            help="lock/unlock (disable/enable) natural spawning",
            choices=SubcommandNaturalSpawn.dict_param_to_bool.keys(),
        )

    dict_param_to_bool: dict[str, bool] = {
        "lock": False,
        "unlock": True,
        "enable": True,
        "disable": False
    }

from commands.base import SubcommandInfo, SubcommandName, DestName


class SubcommandNew(SubcommandInfo):

    @staticmethod
    def get_name():
        return SubcommandName.new

    @staticmethod
    def get_help():
        return "Creates a new simulation"

    @staticmethod
    def form_parser(parser) -> None:
        parser.add_argument(
            "-e", "--empty",
            action="store_true",
            dest=DestName.new_empty,
            help="Do not perform initial entity spawning"
        )

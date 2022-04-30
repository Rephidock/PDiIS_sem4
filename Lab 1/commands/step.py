from commands.base import SubcommandInfo, SubcommandName, DestName


class SubcommandStep(SubcommandInfo):

    @staticmethod
    def get_name():
        return SubcommandName.step

    @staticmethod
    def get_help():
        return "Performs simulation step"

    @staticmethod
    def form_parser(parser) -> None:
        parser.add_argument(
            DestName.step_count,
            action="store",
            help="How many steps to perform",
            type=int,
            default=1,
            nargs='?'
        )

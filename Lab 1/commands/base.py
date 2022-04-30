from __future__ import annotations
from typing import Final
from abc import ABC, abstractmethod
import argparse


class ArgParser:

    def __init__(self):
        # Create base parser
        self.parser = argparse.ArgumentParser(description="A simple animals step simulation on a grid")

        # Add filename
        self.parser.add_argument(
            DestName.filename,
            action="store",
            help="File to work with"
        )

        # Add "flags"
        self.parser.add_argument(
            "-p", "--print",
            action="store_true",
            dest=DestName.print,
            help="Prints the simulation state after subcommand is performed, or current state if no subcommand given"
        )

        self.parser.add_argument(
            "-u", "--uncolored",
            action="store_true",
            dest=DestName.uncolored,
            help="When printing removes any and all color"
        )

        # Create place for subcommands
        self.subparsers = self.parser.add_subparsers(title="subcommands", dest=DestName.subcommand)
        self.parser.set_defaults(subcommand=SubcommandName.nocommand)

    def register_subcommand(self, subcommand: SubcommandInfo) -> None:
        subparser = self.subparsers.add_parser(
            subcommand.get_name(),
            help=subcommand.get_help(),
            description=subcommand.get_help(),
        )
        subcommand.form_parser(subparser)

    def parse(self) -> argparse.Namespace:
        return self.parser.parse_args()

    def parse_list(self, args: list[str]) -> argparse.Namespace:
        return self.parser.parse_args(args)


#region //// Subcommand info base

class SubcommandInfo(ABC):

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_help() -> str:
        pass

    @staticmethod
    @abstractmethod
    def form_parser(parser: argparse.ArgumentParser) -> None:
        pass

#endregion


#region //// Constants (names)

class SubcommandName:
    nocommand: Final[str] = "nocom"
    new: Final[str] = "new"
    place: Final[str] = "place"
    step: Final[str] = "step"
    natural_spawn: Final[str] = "natural"


class DestName:

    # Base
    filename: Final[str] = "filename"
    subcommand: Final[str] = "subcommand"
    print: Final[str] = "flag_print"
    uncolored: Final[str] = "flag_uncolored"

    # New
    new_empty: Final[str] = "create_empty"

    # Place
    place_x: Final[str] = "x"
    place_y: Final[str] = "y"
    place_type: Final[str] = "entity_type"

    # Step
    step_count: Final[str] = "step_count"

    # Natural spawning
    natural_lock: Final[str] = "lock_state"

#endregion

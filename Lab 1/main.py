import commands
import fileio
import zeroplayer
from utils.exceptions import InvalidInputError


def main():

    # Parse params (may exit)
    parser = commands.base.ArgParser()
    parser.register_subcommand(commands.new.SubcommandNew())
    parser.register_subcommand(commands.place.SubcommandPlace())
    parser.register_subcommand(commands.step.SubcommandStep())
    parser.register_subcommand(commands.natural_spawn.SubcommandNaturalSpawn())

    arguments = parser.parse()

    # Path check
    if not fileio.is_path_exists_or_creatable(arguments.filename):
        raise InvalidInputError("invalid filename")

    # New (Will immediately save)
    if arguments.subcommand == commands.base.SubcommandName.new:
        fileio.save_location(
            arguments.filename,
            zeroplayer.animals.location.WoodlandEdge(arguments.create_empty)
        )

    # Load
    if not fileio.is_paths_exists(arguments.filename):
        raise InvalidInputError("no simulation created. Use 'new' to create a new simulation.")

    location = fileio.load_location(arguments.filename)

    # Natural spawn toggle
    if arguments.subcommand == commands.base.SubcommandName.natural_spawn:
        toggle: bool = commands.natural_spawn.SubcommandNaturalSpawn.dict_param_to_bool[arguments.natural_lock]
        location.spawning_enabled = toggle

    # Step
    elif arguments.subcommand == commands.base.SubcommandName.step:
        count: int = arguments.step_count

        if count < 1:
            raise InvalidInputError("invalid step count")

        for _ in range(count):
            location.step()

    # Place
    elif arguments.subcommand == commands.base.SubcommandName.place:
        if arguments.x < 0 or arguments.x >= location.width or arguments.y < 0 or arguments.y >= location.height:
            raise InvalidInputError("placement out of range")

        entity = commands.place.SubcommandPlace.dict_param_to_type[arguments.entity_type]()
        entity.place_at(location, arguments.x, arguments.y)

    # Print
    if arguments.flag_print or arguments.subcommand == commands.base.SubcommandName.nocommand:
        zeroplayer.display.print_location(
            location,
            not arguments.flag_uncolored
        )

    # Save
    fileio.save_location(arguments.filename, location)


if __name__ == '__main__':
    try:
        main()
    except InvalidInputError as ex:
        print(f"error: {ex}")
        exit()

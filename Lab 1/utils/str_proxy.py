from typing import Any, Type, Callable


def str_proxy(obj: Any, overrides: dict[Type, Callable[[Any], str]]) -> str:
    """
    str() with overwrites.

    A single override only works for specified classes,
    not any of the child classes.
    """

    # Try to find override
    lookup = overrides.get(type(obj))

    # No override
    if lookup is None:
        return str(obj)

    # Perform override
    return lookup(obj)

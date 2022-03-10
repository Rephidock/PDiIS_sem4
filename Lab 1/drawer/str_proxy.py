from typing import Any, Type, Callable
import zeroplayer


__overrides: dict[Type, Callable[[Any], str]] = {
    zeroplayer.entity.Entity: lambda: "Entity",
    zeroplayer.resource.Resource: lambda obj: f"Resource[{obj.value}, {obj.decay_speed}]"
}


def str_proxy(obj: Any) -> str:
    # Try to find override
    lookup = __overrides.get(type(obj))

    # No override
    if lookup is None:
        return str(obj)

    # Perform override
    return lookup(obj)

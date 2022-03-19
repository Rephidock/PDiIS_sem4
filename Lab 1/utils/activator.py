from typing import Type, Any


def create_instance(inst_type: Type, args: tuple[Any, ...]) -> Any:
    return inst_type(*args)

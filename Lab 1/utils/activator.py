from typing import Type, Any


def create_instance(inst_type: Type, *args: Any) -> Any:
    return inst_type(*args)

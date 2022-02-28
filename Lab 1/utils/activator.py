from __future__ import annotations
from typing import Type, Any


class Activator:

    @staticmethod
    def create_instance(inst_type: Type, *args: Any):
        return inst_type(*args)

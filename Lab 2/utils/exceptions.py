from typing import Any


class InvalidOperationError(RuntimeError):
    """Raised when an operation is performed when object is in invalid state for that operation"""
    pass


class VersionMismatchError(RuntimeError):
    """Raised when there is a fatal mismatch in versions during an operation"""
    def __init__(self, given: Any = "?", expected: Any = "?", message: str = ""):
        super().__init__(f"{message}. Expected version {expected}. Given version. {given}")


class InvalidInputError(RuntimeError):
    """Raised when user input is invalid"""
    pass


class InvalidPathError(RuntimeError):
    """Raised when given path is invalid"""
    pass

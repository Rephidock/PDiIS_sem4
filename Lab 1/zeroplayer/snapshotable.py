from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod


class Snapshotable(ABC):

    def form_snapshot(self) -> Snapshot:
        """Creates a new snapshot, fills it and returns it."""
        snapshot = Snapshot()
        self.fill_snapshot(snapshot)
        return snapshot

    @abstractmethod
    def fill_snapshot(self, snapshot: Snapshot):
        """
        Adds data to the snapshot.
        Use super calls during inheritance.
        Virtual.
        """
        pass

    @abstractmethod
    def restore_from_snapshot(self, snapshot: Snapshot):
        """
        Uses a snapshot to restore state.
        Virtual.
        """
        pass


class Snapshot:

    data: dict[type, dict[str, Any]]  # Stores data per type

    def __init__(self):
        self.data = dict()

    def set_data(self, cls: type | None, key: str, data: Any):
        """Sets data under specified class under specified key."""

        # None
        if cls is None: cls = type(None)

        # Get/Create lump (dict for desired class)
        lump = self.data.get(cls, None)
        if lump is None:
            lump = dict()
            self.data[cls] = lump

        # Set data
        lump[key] = data

    def get_data(self, cls: type | None, key: str, default: Any = None) -> Any:
        """Reads data under specified class under specified key"""

        # None
        if cls is None: cls = type(None)

        # Get lump
        lump = self.data.get(cls, None)
        if lump is None: return default

        # Return data
        return lump.get(key, default)

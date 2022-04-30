from utils.action_queue import ActionPriorityQueue
from abc import ABCMeta

from zeroplayer.location import Location
from zeroplayer.step_priorities import StepPriority

from zeroplayer.snapshotable import Snapshotable, Snapshot


class Entity(Snapshotable, metaclass=ABCMeta):
    """Base class for all entities."""

    def __init__(self):
        self.__lifetime = 0
        self.__init_location()

    def step(self, action_queue: ActionPriorityQueue) -> None:
        """
        Enqueues all actions from this entity
        Should be extended by children via super.
        """
        action_queue.enqueue(StepPriority.LIFETIME, self.__action_increase_lifetime)

    #region //// Lifetime

    __lifetime: int

    def __action_increase_lifetime(self):
        self.__lifetime += 1

    @property
    def lifetime(self) -> int:
        return self.__lifetime

    #endregion

    #region //// Location

    # Stores placement of self in the location
    # Link is 2 way
    # Link is **not** saved in the snapshot

    __location: Location | None
    __x: int
    __y: int

    def __init_location(self):
        self.__location = None
        self.__x = 0
        self.__y = 0

    def place_at(self, location: Location, x: int, y: int):
        """Moves entity to a position and or location"""

        # Remove at old
        if self.__location is not None:
            self.__location[self.__x, self.__y] = None

        # Place at new
        self.__location = location
        self.__x, self.__y = self.__location.clamp_position(x, y)

        if self.__location[self.__x, self.__y] is not None:
            self.__location[self.__x, self.__y].remove()  # Remove already present entity
        self.__location[self.__x, self.__y] = self

    def remove(self):
        """Remove entity from current location. Does not change x and y positions."""
        if self.__location is not None:
            self.__location[self.__x, self.__y] = None
        self.__location = None

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def location(self) -> Location:
        return self.__location

    #endregion

    #region //// Snapshot

    def fill_snapshot(self, snapshot: Snapshot):
        snapshot.set_data(Entity, "lifetime", self.__lifetime)

    def restore_from_snapshot(self, snapshot: Snapshot):
        self.__lifetime = snapshot.get_data(Entity, "lifetime")

    #endregion

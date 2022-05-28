from records.record import Teacher as Record
from records.record import TeacherFieldOptions as RecordFieldOptions
from records.fileio import XMLReadWriter, PathChecker
from typing import Callable, Iterable
from utils import exceptions


class RecordKeeper:
    """
    A class designed to store and work with records.
    At it's core - a list of records.
    Supports operator[] and iteration.
    """

    __storage: list[Record]
    __field_options: RecordFieldOptions
    __filepath: str

    def __init__(self):
        self.__storage = []
        self.__field_options = RecordFieldOptions()
        self.__filepath = ""

    #region //// Saving, Loading

    @property
    def filepath(self) -> str:
        return self.__filepath

    def set_filepath(self, path: str):
        if not PathChecker.is_pathname_valid(path):
            raise exceptions.InvalidPathError()
        self.__filepath = path

    def save(self):
        """Saves records under current file path"""
        # Check path
        if not PathChecker.is_path_exists_or_creatable(self.__filepath):
            raise exceptions.InvalidPathError()
        # Write
        XMLReadWriter.write(self.__filepath, self.__storage)

    def load(self):
        """Load records from current file path"""
        # Check path
        if not PathChecker.is_paths_exists(self.__filepath):
            raise FileNotFoundError()
        # Read
        self.__storage = XMLReadWriter.read(self.__filepath)
        self.__field_options = RecordFieldOptions()
        self.__field_options.add_options_from(*self.__storage)

    #endregion

    #region //// Read and edit records

    def __getitem__(self, index: int) -> Record:
        if index < 0 or index >= len(self.__storage):
            raise IndexError("Storage index out of range")
        return self.__storage[index]

    def __setitem__(self, index: int, value: Record):
        if index < 0 or index >= len(self.__storage):
            raise IndexError("Storage index out of range")
        self.__storage[index] = value
        self.__field_options.add_options_from(value)

    def __iter__(self):
        for record in self.__storage:
            yield record

    @property
    def count(self) -> int:
        """Returns how many records are currently stored"""
        return len(self)

    def __len__(self) -> int:
        return len(self.__storage)

    def add(self, *records: Record):
        """Appends item(s) to the end of the record storage"""
        self.__storage.extend(records)
        self.__field_options.add_options_from(*records)

    def remove_at(self, index: int):
        """Removes item at index"""
        if index < 0 or index >= len(self.__storage):
            raise IndexError("Storage index out of range")
        self.__storage.pop(index)

    def clear(self):
        """Removes all records"""
        self.__storage.clear()
        self.__field_options = RecordFieldOptions()

    #endregion

    #region //// Search

    def search(self, *predicates: Callable[[Record], bool]) -> Iterable[int]:
        """
        Returns indexes of records for which all given predicates return True.
        May break if records are altered mid-iteration
        """
        for i, record in enumerate(self.__storage):
            ret = True
            for predicate in predicates:
                if ret is False: break
                ret = ret and predicate(record)
            if ret is True: yield i

    def search_and_remove(self, *predicates: Callable[[Record], bool]) -> int:
        """
        Removes all records for which all given predicates return True
        Returns how many records were removed
        """
        indexes_to_remove = set(self.search(*predicates))
        self.__storage[:] = [x for i, x in enumerate(self.__storage) if i not in indexes_to_remove]
        return len(indexes_to_remove)

    #endregion

    #region //// Field Options

    @property
    def field_options(self):
        return self.__field_options

    #endregion

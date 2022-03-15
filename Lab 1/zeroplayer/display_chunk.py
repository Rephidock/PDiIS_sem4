from __future__ import annotations
from typing import Optional, Callable, Any
from utils.string_utils import str_proxy, str_replace_at
from zeroplayer.entities.entity import Entity


class DisplayChunk:

    # Defaults
    border_set_default: str = "╔═╗║ ║╚═╝[]"
    name_default = "Unnamed"

    # Instance
    __name: str
    content_chunks: list[DisplayChunk]
    content_singles: list[str]
    __width: int
    __height: int
    __border_set: str

    def __init__(self):
        # Name
        self.__name = self.name_default

        # Content
        self.content_chunks = list()
        self.content_singles = list()
        self.__width = 0
        self.__height = 0

        # Border
        self.__border_set = self.border_set_default

    # region //// From entity

    @classmethod
    def from_entity(
            cls,
            entity: Entity,
            overrides: Optional[dict[type, Callable[[Any], str]]] = None
    ) -> str | DisplayChunk:
        """
        Creates a display chunk or string from an entity.
        Uses str_proxy.
        Recursively applies to all children of given entity.
        A chunk is created for each entity that has children.
        """

        # Defaults
        if overrides is None:
            overrides = dict()

        # String
        if not entity.children:  # Empty dictionary will evaluate to False
            return str_proxy(entity, overrides)

        # Chunk
        ret = DisplayChunk()
        ret.set_name(str_proxy(entity, overrides))

        for child in entity.children.values():
            ret.add_content(DisplayChunk.from_entity(child, overrides=overrides))

        return ret

    # endregion

    #region //// Setters, Add content

    def set_name(self, name: str) -> DisplayChunk:
        """Returns self"""
        self.__name = name
        return self

    def set_border(self, border_set: str) -> DisplayChunk:
        """
        Borders are strings with characters in this order:
        tl, tm, tr, ml, mm, mr, bl, bm, br, name_left, name_right.
        Returns self.
        """
        self.__border_set = border_set
        if len(border_set) < 11:
            raise ValueError("Border set must contain 11 characters")
        return self

    def add_content(self, content: str | DisplayChunk) -> DisplayChunk:
        """
        Returns self.
        """
        if content is str:
            self.content_singles.append(content)

        if content is DisplayChunk:
            self.content_chunks.append(content)

        return self

    #endregion

    #region //// Width, height

    def __calc_dims(self):

        # Name
        self.__width = len(self.__name) + 2  # (2 for name edges)
        self.__height = 0

        # Nested content
        chunks_total_width = 0
        chunks_max_height = 0
        for nest in self.content_chunks:
            nest.__calc_dims()
            chunks_total_width += nest.__width
            chunks_max_height = max(chunks_max_height, nest.__height)

        self.__width = max(self.__width, chunks_total_width)
        self.__height += chunks_max_height

        # Singles content
        self.__height += len(self.content_singles)
        for s in self.content_singles:
            self.__width = max(self.__width, len(s))

        # Border
        self.__height += 2
        self.__width += 2

    #endregion

    #region //// To String

    def get_strings(self) -> list[str]:

        # Create border
        self.__calc_dims()

        rows = [
            self.__border_set[3] + self.__border_set[4] * (self.__width - 2) + self.__border_set[5]
            for _ in range(self.__height-2)   # -2: top and bottom rows
            ]
        rows.insert(0,  self.__border_set[0] + self.__border_set[1] * (self.__width - 2) + self.__border_set[2])
        rows.append(self.__border_set[6] + self.__border_set[7] * (self.__width - 2) + self.__border_set[8])

        # Name
        rows[0] = str_replace_at(rows[0], 1, self.__border_set[9] + self.__name + self.__border_set[10])

        # Content: Nests
        curx = 1
        for chunk in self.content_chunks:
            chunk_strings = chunk.get_strings()
            for i, chunk_row in enumerate(chunk_strings):
                rows[i + 1] = str_replace_at(rows[i + 1], curx, chunk_row)
            curx += chunk.__width

        # Content: Singles
        offset = self.__height - len(self.content_singles) - 1
        for i, single in enumerate(self.content_singles):
            rows[i + offset] = str_replace_at(rows[i + offset], 1, single)

        # Return
        return rows

    def __str__(self):
        return "\n".join(self.get_strings())

    #endregion

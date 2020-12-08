import re
from typing import List

from .base import Node
from ..utils import EmptyConfig


class Group(Node):
    """
    starts with
        any number of spaces
            [
                :name - alpha numeric, containing at least one character
            ]
        any number of spaces or comments
    end
    """

    REGEX = re.compile("^\s*\[(?P<name>[a-zA-Z0-9]+)\]\s*(;.*)?$")

    def __init__(self, scanner, name: str, start: int, overrides: List[str] = None):
        self.name = name
        self.scanner = scanner
        self.properties = {}

        self.overrides = overrides or []

        self.start = start
        self.end = None
        self._hash = ""

    @classmethod
    def parse(cls, scanner: "Scanner", line: str, start: int, overrides: List[str] = None) -> "Group":
        """
        Exctract helpful data from current line.

        :param scanner: Scanner instance. Used to re-index properties and check if the current group is 1:1 with it's origin.
        :param line: Current line being parsed.
        :param start: Absolute position in the file.
        :param overrides: List of accepted overrides.
        :return: group
        """

        match = cls.REGEX.match(line)
        return cls(scanner, match.group("name"), start, overrides)

    @property
    def is_fresh(self) -> bool:
        """
        Compare current content with file's group content.

        :return: bool
        """

        return self._hash == self.scanner.compute_hash(self.start, self.end)

    def ends(self, end: int):
        """
        Mark the end of the group. Compute it's current hash.

        :param end: Position of the last byte in file.
        :return: None
        """

        self.end = end
        self._hash = self.scanner.compute_hash(self.start, self.end)

    def index(self):
        """
        Scan over the current group and add it's properties in memory.
        Store overrides as well.

        :return: None
        """

        for property in self.scanner.fill_group(self.start, self.end):
            if property.override:
                self.properties[f"{property.name}-{property.override}"] = property.value
            else:
                self.properties[property.name] = property.value

    def get(self, name: str, indexed: bool = False):
        """
        Return property from local cache. If missing, re-index the group. Take into account overrides.

        :param name: Property name.
        :param indexed: Mark if was recently indexed. If not and the property is missing, re-index.
        :return: Property's value.
        """

        # compute property's keys, taking into account the overrides.
        keys = [f"{name}-{override}" for override in self.overrides] + [name]
        for key in keys:
            if key in self.properties:
                return self.properties.get(key)

        # if the property is still missing, after re-index, don't fail, but return EmptyConfig
        if indexed:
            return EmptyConfig()

        # search for missing property
        self.index()

        return self.get(name, indexed=True)

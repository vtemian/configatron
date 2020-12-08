import re
from typing import List

from ..utils import EmptyConfig


class Group:
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
    def parse(cls, parser, line: str, start: int, overrides: List[str] = None):
        match = cls.REGEX.match(line)
        return cls(parser, match.group("name"), start, overrides)

    @classmethod
    def is_valid(cls, line):
        return cls.REGEX.match(line) is not None

    @property
    def is_fresh(self):
        return self._hash == self.scanner.compute_hash(self.start, self.end)

    def ends(self, end: int):
        self.end = end
        self._hash = self.scanner.compute_hash(self.start, self.end)

    def index(self):
        for property in self.scanner.fill_group(self.start, self.end):
            if property.override:
                self.properties[f"{property.name}-{property.override}"] = property.value
            else:
                self.properties[property.name] = property.value

    def get(self, name: str, indexed: bool = False):
        keys = [f"{name}-{override}" for override in self.overrides] + [name]
        for key in keys:
            if key in self.properties:
                return self.properties.get(key)

        if indexed:
            return EmptyConfig()

        self.index()

        return self.get(name, indexed=True)

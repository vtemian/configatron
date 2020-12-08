import re

from ..utils import EmptyConfig


class Group:
    REGEX = re.compile("^\s*\[(?P<name>[a-zA-Z0-9]+)\]\s*(;.*)?$")

    def __init__(self, scanner, name: str, start: int, end: int = None):
        self.name = name
        self.scanner = scanner
        self.properties = {}

        self.start = start
        self.end = end
        self._hash = ""

    @classmethod
    def parse(cls, parser, line: str, start: int):
        match = cls.REGEX.match(line)
        return cls(parser, match.group("name"), start)

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
            self.properties[property.name] = property.value

    def get(self, name: str):
        if name not in self.properties:
            self.index()

        if name not in self.properties:
            return EmptyConfig()

        return self.properties.get(name)

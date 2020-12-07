import logging
import os
import re


def string(value: str):
    if not all([
        value.startswith("\""),
        value.endswith("\""),
        "\"" not in value[1:-1] or "\\\"" in value[1:-1]
    ]):
        return None

    return value[1:-1]


def path(value: str):
    if value[0] is not "/":
        return None

    return value


def number(value: str):
    if value.isdigit():
        return int(value)

    if value.lstrip('-').replace('.', '').isdigit():
        return float(value)

    return None


def boolean(value: str):
    if value in {'"yes"', '"no"', '"true"', '"false"', "0", "1"}:
        return value in {'"yes"', '"true"', "1"}

    return None


def array(value: str):
    if "," in value and not value.startswith("\"") and not value.endswith("\""):
        return value.split(",")

    return None


properties = [
    string, path, number, boolean, array
]


class Comment:
    REGEX = re.compile('^\s*(;.*)?$')

    @classmethod
    def is_valid(cls, line):
        return cls.REGEX.match(line) is not None


class Group:
    REGEX = re.compile('^\s*\[(?P<name>\w*)\]\s*(;.*)?$')

    def __init__(self, parser, name: str, start: int, end: int = None):
        self.name = name
        self.parser = parser
        self.properties = {}
        self.content = ""

        self.position = {
            "start": start,
            "end": end
        }

    @classmethod
    def parse(cls, parser, line: str, start: int):
        match = cls.REGEX.match(line)
        return cls(parser, match.group("name"), start)

    @classmethod
    def is_valid(cls, line):
        return cls.REGEX.match(line) is not None

    def add(self, property: 'Property'):
        self.properties[property.name] = property

    def ends(self, end: int):
        self.position["end"] = end

    def get(self, name: str):
        if name not in self.properties:
            self.parser.index_group(self)

        if name not in self.properties:
            raise ValueError("Missing property from group")

        return self.properties.get(name)


class Property:
    REGEX = re.compile('^\s*(?P<name>\w*)\s*=\s*(?P<value>[a-zA-Z-0-9/"]*)\s*(;.*)?$')

    def __init__(self, name: str, value: str, start: int, end: int):
        self.name = name
        self.value = value

        self.position = [start, end]

    @classmethod
    def parse(cls, line: str, start: int):
        end = len(line) + start
        match = cls.REGEX.match(line)
        value = None

        for kind in properties:
            value = kind(match.group("value"))
            if value:
                break

        return cls(match.group("name"), value, start, end)

    @classmethod
    def is_valid(cls, line):
        match = cls.REGEX.match(line)
        if match is None:
            return False

        for kind in properties:
            if kind(match.group("value")):
                return True

        return False

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Property):
            return other.value == self.value

        return other == self.value


class Configurator:
    def __init__(self, source: str):
        self.source = source
        self.groups = {}

        self._current_group = None

        if not os.path.exists(self.source):
            raise RuntimeError(f"Missing {self.source} file")

        self.source_key = None
        self.index_groups()
        self.source_key = os.stat(self.source).st_mtime

    def should_index(self):
        return self.source_key != os.stat(self.source).st_mtime

    def index_groups(self):
        if not self.should_index():
            logging.debug(f"Nothing to index for {self.source}")
            return

        for start, end, line in self.read():
            self.parse(start, line)

    def index_group(self, group):
        with open(self.source) as config:
            config.seek(group.position["start"])
            start = group.position["start"]

            for line in config.read(group.position["end"] - group.position["start"]).splitlines():
                if not Property.is_valid(line):
                    raise ValueError("invalid config")

                group.add(Property.parse(line, start))

                start += len(line)

    def read(self):
        start = 0

        with open(self.source) as config:
            for line in config.readlines():
                end = start + len(line)

                yield start, end, line

                start = end

            if self._current_group:
                self._current_group.ends(end)

    def parse(self, start, line):
        if Group.is_valid(line):
            if self._current_group:
                self._current_group.ends(start)

            self._current_group = Group.parse(self, line, start + len(line))
            self.groups[self._current_group.name] = self._current_group

        elif Property.is_valid(line):
            if not self._current_group:
                raise ValueError("invalid property")

        elif not Comment.is_valid(line):
            raise ValueError(f"invalid config {line}")

        if self._current_group:
            self._current_group.content += line

    def get(self, group_name: str):
        if group_name not in self.groups:
            self.index_groups()

        if group_name not in self.groups:
            raise ValueError("Missing group")

        return self.groups.get(group_name)
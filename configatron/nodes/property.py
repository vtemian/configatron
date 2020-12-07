import re


def string(value: str):
    if all([
        value.startswith("\""),
        value.endswith("\""),
        "\"" not in value[1:-1] or "\\\"" in value[1:-1]
    ]):
        return value[1:-1]

    return


def path(value: str):
    if value[0] == "/":
        return value

    return None


def number(value: str):
    if value.lstrip('-').isdigit():
        return int(value)

    if value.lstrip('-').replace('.', '').isdigit():
        return float(value)

    return None


def boolean(value: str):
    if value in {'yes', 'no', 'true', 'false', "0", "1"}:
        return value in {'yes', 'true', "1"}

    return None


def array(value: str):
    if "," in value and not value.startswith("\"") and not value.endswith("\""):
        return value.split(",")

    return None


properties = [
    array, boolean, number, path, string
]


class Property:
    REGEX = re.compile('^\s*(?P<name>\w*)\s*=\s*(?P<value>[a-zA-Z0-9/",]*)\s*(;.*)?$')

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    @classmethod
    def parse(cls, line: str):
        match = cls.REGEX.match(line)
        if not match:
            return

        for kind in properties:
            value = kind(match.group("value"))
            if value is not None:
                return cls(match.group("name"), value)

    @classmethod
    def is_valid(cls, line):
        match = cls.REGEX.match(line)
        if match is None:
            return False

        for kind in properties:
            if kind(match.group("value")) is not None:
                return True

        return False

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Property):
            return other.value == self.value

        return other == self.value

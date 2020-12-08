import os
import re
from typing import Optional, Union, List

from .base import Node


def string(value: str) -> Optional[str]:
    """
    Check if the value is a string.
    """

    if all([value.startswith('"'), value.endswith('"'), '"' not in value[1:-1] or '\\"' in value[1:-1]]):
        return value[1:-1]

    return


def path(value: str) -> Optional[str]:
    """
    Check if the current value is a path. Paths need to be absolute
    """

    if len(value) > 0 and value[0] == "/":
        return os.path.abspath(value)

    return None


def number(value: str) -> Union[int, float, None]:
    """
    Check if the current number is an int or float.
    """

    if value.lstrip("-").isdigit():
        return int(value)

    if value.lstrip("-").replace(".", "").isdigit():
        return float(value)

    return None


def boolean(value: str) -> Optional[bool]:
    """
    Check if the current value is a boolean value:
        true: yes, true, 1
        false: no, false, 0
    """

    if value in {"yes", "no", "true", "false", "0", "1"}:
        return value in {"yes", "true", "1"}

    return None


def array(value: str) -> Optional[List[any]]:
    """
    Check if the current value is an array.
    """

    if "," in value and not value.startswith('"') and not value.endswith('"'):
        return value.split(",")

    return None


properties = [array, boolean, number, path, string]


class Property(Node):
    """
    starts with
        any number of spaces
            :name - at least one letter, - or _
                can be followed by
                    <
                        :override - at least one letter, - or _
                    >
        any number of spaces
            =
        any number of spaces
            :value - at least one letter, number, or /.,
        any number of spaces or comments
    end
    """

    REGEX = re.compile(
        '^\s*(?P<name>[a-zA-Z_-]+)(<(?P<override>[a-zA-Z_-]+)>)?\s*=\s*(?P<value>[a-zA-Z0-9-/,\."]+)\s*(;.*)?$'
    )

    def __init__(self, name: str, value: str, override: str = None):
        self.name = name
        self.value = value
        self.override = override

    @classmethod
    def parse(cls, line: str) -> Optional["Property"]:
        """
        Parse the current line and try to extract the true value.

        :param line: Current line being processed.
        :return: Property or None
        """

        match = cls.REGEX.match(line)
        if not match:
            return

        for kind in properties:
            value = kind(match.group("value"))
            if value is not None:
                return cls(match.group("name"), value, match.group("override"))

    @classmethod
    def is_valid(cls, line: str) -> bool:
        """
        Check if a the current line holds a property or not.

        :param line: Current line being processed.
        :return: bool
        """

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

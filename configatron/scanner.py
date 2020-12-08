import hashlib
from typing import List

from configatron.errors import ValidationError
from configatron.nodes.comment import Comment
from configatron.nodes.group import Group
from configatron.nodes.property import Property


class Scanner:
    def __init__(self, reader, overrides: List[str] = None):
        self.reader = reader
        self.overrides = overrides

    def groups(self, validate: bool = True):
        """
        Scan the reader and parse all the groups.
        Can throw exceptions if the scheme is not valid.

        :param validate: Throws exceptions if the scheme is not valid
        :return: None
        """

        current_group = None

        for start, end, line in self.reader.lines():
            if Group.is_valid(line):
                # Found a new group, so we can yield any currently building group
                if current_group:
                    yield current_group

                current_group = Group.parse(self, line, start + len(line), self.overrides)
            elif validate:
                # check for valid properties
                if "=" in line:
                    if not Property.is_valid(line) or not current_group:
                        raise ValidationError(f"Invalid property: {line}")

                # check for valid comments and whitespaces
                elif not Comment.is_valid(line):
                    raise ValidationError(f"Invalid config: {line}")

            if current_group:
                current_group.ends(end)

        # Check for any groups that are currently building
        if current_group:
            yield current_group

    def compute_hash(self, start: int, end: int) -> str:
        """ Compute hash over a block. """

        return hashlib.sha256(self.reader.block(start, end).encode())

    def fill_group(self, start: int, end: int) -> Property:
        """
        Scan a certain group and add properties to it.

        :param start: start byte
        :param end: end byte
        :return: yields properties
        """

        for line in self.reader.block(start, end).split("\n"):
            if Property.is_valid(line):
                yield Property.parse(line)

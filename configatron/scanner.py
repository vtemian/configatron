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
        current_group = None

        for start, end, line in self.reader.lines():
            if Group.is_valid(line):
                if current_group:
                    yield current_group

                current_group = Group.parse(self, line, start + len(line), self.overrides)

            elif validate:
                if "=" in line:
                    if not Property.is_valid(line) or not current_group:
                        raise ValidationError(f"Invalid property: {line}")

                elif not Comment.is_valid(line):
                    raise ValidationError(f"Invalid config: {line}")

            if current_group:
                # TODO: Don't compute the content hash each time
                current_group.ends(end)

        if current_group:
            yield current_group

    def compute_hash(self, start, end):
        return hashlib.sha256(self.reader.block(start, end).encode())

    def fill_group(self, start, end):
        for line in self.reader.block(start, end).split("\n"):
            if Property.is_valid(line):
                yield Property.parse(line)

import re


class Comment:
    REGEX = re.compile("^(\n)|(\s*(;.*)?)$")

    @classmethod
    def is_valid(cls, line):
        return cls.REGEX.match(line) is not None

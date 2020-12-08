class Node:
    @classmethod
    def is_valid(cls, line: str) -> bool:
        return cls.REGEX.match(line) is not None

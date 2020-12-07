import os

from .base import BaseReader
from .errors import InvalidSource


class FileReader(BaseReader):
    def read(self):
        if not os.path.exists(self.source):
            raise InvalidSource(f"Missing {self.source} file")

        with open(self.source) as config:
            for line in config.readline():
                yield line


class CachedFileReader(FileReader):
    def read(self):
        content = []

        for line in super().read():
            content.append(line)

            yield line

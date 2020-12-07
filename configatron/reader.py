import os


class Reader:
    def __init__(self, source: str):
        self.source = source

    def block(self, start: int, end: int = None):
        if not os.path.exists(self.source):
            raise RuntimeError(f"Missing {self.source} file")

        with open(self.source) as config:
            config.seek(start)

            if end is not None:
                return config.read(end - start)

            return config.read()

    def lines(self, start: int = 0):
        if not os.path.exists(self.source):
            raise RuntimeError(f"Missing {self.source} file")

        with open(self.source) as config:
            config.seek(start)

            for line in config.readlines():
                end = start + len(line)
                yield start, end, line
                start = end

import os


class Reader:
    def __init__(self, source: str):
        if not os.path.exists(source):
            raise RuntimeError(f"Missing {self.source} file")

        self.source = source

    def block(self, start: int, end: int = None) -> str:
        """
        Reads a block of data, within an interval.

        :param start: start byte
        :param end: end byte
        :return: read block of bytes.
        """

        with open(self.source) as config:
            config.seek(start)

            if end is not None:
                return config.read(end - start)

            return config.read()

    def lines(self, start: int = 0) -> str:
        """
        Reads line by line. Yield a line once is read. Keep the file open until all is read.

        :param start: start byte
        :return: yield lines from the file
        """

        with open(self.source) as config:
            config.seek(start)

            for line in config.readlines():
                end = start + len(line)
                yield start, end, line
                start = end

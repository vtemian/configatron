from abc import abstractmethod, ABCMeta


class BaseReader(metaclass=ABCMeta):
    def __init__(self, source: str):
        self.source = source

    @abstractmethod
    def read(self):
        raise NotImplemented

from abc import abstractmethod, ABCMeta


class BaseParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self):
        raise NotImplemented

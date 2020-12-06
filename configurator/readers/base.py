from abc import abstractmethod, ABCMeta


class BaseReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        raise NotImplemented

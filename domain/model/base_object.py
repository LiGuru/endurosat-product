from abc import ABC, abstractmethod, abstractproperty


class BaseObject(ABC):

    def __init__(self, address):
        self.__address = address

    @property
    @abstractmethod
    def REGISTER(self):
        raise NotImplemented

    @abstractmethod
    def decoder(self, *args):
        raise NotImplemented

    def encoder(self, *args):
        raise NotImplemented

    def set_address(self, address: str) -> None:
        self.__address = address

    def get_address(self):
        return self.__address

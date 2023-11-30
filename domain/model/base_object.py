from abc import ABC, abstractmethod


class BaseObject(ABC):

    def __init__(self, address):
        self.__address = address

    @abstractmethod
    def set_dimensions(self, *args):
        raise NotImplemented

    def set_address(self, address: str) -> None:
        self.__address = address

    def get_address(self):
        return self.__address

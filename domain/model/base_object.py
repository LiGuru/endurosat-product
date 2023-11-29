from abc import ABC, abstractmethod


class BaseObject(ABC):

    def __init__(self, address):
        self.address = address

    @abstractmethod
    def set_dimensions(self, *args):
        raise NotImplemented

    def set_address(self, address: str) -> None:
        self.address = address

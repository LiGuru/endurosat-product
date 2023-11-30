from abc import ABC, abstractmethod


class BaseEncoder(ABC):

    @abstractmethod
    def encoder(self, msg, mode: str, *, args):
        raise NotImplemented



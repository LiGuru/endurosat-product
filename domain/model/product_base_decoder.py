from abc import ABC, abstractmethod


class BaseDecoder(ABC):

    @abstractmethod
    def decoder(self, msg):
        raise NotImplemented

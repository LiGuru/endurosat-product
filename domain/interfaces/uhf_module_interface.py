from abc import ABC, abstractmethod


class UHFModuleInterface(ABC):
    @abstractmethod
    def set_mode(self, mode: int):
        pass

    @abstractmethod
    def send_command(self, command: str) -> str:
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass

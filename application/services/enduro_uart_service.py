from typing import Callable

from external_services.uart.uart_service import UARTService
from infrastructure.commons.transform_data import DictToObj
from infrastructure.logging.infrastructure_logger import ProgramLogger


class EnduroUARTService:

    def __init__(self, config: DictToObj, slogger: ProgramLogger, callback: Callable = None):
        self.uart = None
        self.__config = config
        self.__slogger = slogger
        self.__callback: Callable = callback if callback else self.default_callback

    @property
    def callback(self):
        return self.__callback

    @callback.setter
    def callback(self, function: Callable):
        self.__callback = function

    def default_callback(self, data: list):
        pass

    def open(self):
        self.start() if not self.uart else None
        if self.uart:
            try:
                self.uart.open()
            except Exception as e:
                self.__slogger.critical(f"{self.__class__.__name__} -> {str(e)}")
        else:
            raise

    def close(self):
        if self.uart.is_open():
            self.uart.close()

    def start(self):
        if self.uart:
            self.uart = None

        self.uart = UARTService(self.__config.port,
                                self.callback,
                                int(self.__config.baudrate),
                                int(self.__config.bits), int(self.__config.stopbits),
                                None,
                                None,
                                int(self.__config.timeout))

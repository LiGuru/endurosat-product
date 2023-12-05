from typing import Callable

from application.services.enduro_uart_service import EnduroUARTService
from domain.model.base_object import BaseObject
from infrastructure.commons.transform_data import DictToObj
from infrastructure.logging.infrastructure_logger import ProgramLogger


class EnduroUartCommunication:

    def __init__(self, uart, config: DictToObj, slogger: ProgramLogger, callback: Callable = None):
        self.__callback = callback
        self.__conf = config
        self.ser: EnduroUARTService = uart

    @staticmethod
    def encode_data(module: BaseObject, mode):
        return module.encoder(mode)

    def decode_data(self, module: BaseObject, data, mode: str):
        data = module.decoder(data, mode)
        self.__callback(data) if self.__callback else None
        return data

    def execute(self, module: BaseObject, mode: str = 'r'):
        if not isinstance(module, BaseObject):
            raise
        carriage = self.__conf.carriage if hasattr(self.__conf, "carriage") else ''
        msg: str = self.encode_data(module, mode).encode('ascii')
        self.ser.open()
        self.ser.uart.send_message(msg, carriage=carriage)
        response = self.decode_data(module,
                                    self.ser.uart.read_line_based_message(pack_size=22 * 2, carriage=carriage),
                                    mode)
        self.ser.close()
        self.__callback(response) if self.__callback else None

        return response

from typing import Callable

from application.services.enduro_uart_service import EnduroUARTService
from domain.model.decoders.enduro_uhf_protocol_decoder import EnduroUartUHFDecoder
from domain.model.encoders.enduro_uhf_protocol_encoder import EnduroUartUHFEncoder
from domain.model.hardware.uhf_module import UHFModule
from infrastructure.commons.transform_data import DictToObj
from infrastructure.logging.infrastructure_logger import ProgramLogger


class EnduroUartUHFCommunication(EnduroUARTService):

    def __init__(self, config: DictToObj, slogger: ProgramLogger, callback: Callable = None):
        super().__init__(config, slogger, callback)
        self.__callback = callback
        self.__protocol_encoder = EnduroUartUHFEncoder()
        self.__protocol_decoder = EnduroUartUHFDecoder()

    def encode_data(self, uhf_module: UHFModule, mode):
        return self.__protocol_encoder.encoder(uhf_module, mode)

    def decode_data(self, data, mode: str):
        return self.__protocol_decoder.decoder(data, mode)

    def push_data(self, module: UHFModule, mode: str = 'r'):
        self.uart.send_message(self.encode_data(module, mode))
        response = self.decode_data(self.uart.read_message(), mode)
        self.__callback(response) if self.__callback else None

        return response




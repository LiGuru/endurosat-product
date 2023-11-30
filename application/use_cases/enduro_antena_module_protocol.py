from typing import Callable

from application.services.enduro_uart_service import EnduroUARTService
from domain.model.decoders.enduro_antenna_protocol_decoder import EnduroUartAntennaDecoder
from domain.model.encoders.enduro_antenna_protocol_encoder import EnduroUartAntennaEncoder
from domain.model.hardware.antenna_module import AntennaModule
from infrastructure.commons.transform_data import DictToObj
from infrastructure.logging.infrastructure_logger import ProgramLogger


class EnduroUartAntennaCommunication(EnduroUARTService):

    def __init__(self, config: DictToObj, slogger: ProgramLogger, callback: Callable = None):
        super().__init__(config, slogger, callback)
        self.__callback = callback
        self.__protocol_encoder = EnduroUartAntennaEncoder()
        self.__protocol_decoder = EnduroUartAntennaDecoder()

    def encode_data(self, antenna_module: AntennaModule, mode):
        return self.__protocol_encoder.encoder(antenna_module, mode)

    def decode_data(self, data, mode: str):
        return self.__protocol_decoder.decoder(data, mode)

    def push_data(self, module: AntennaModule, mode: str = 'r'):
        self.uart.send_message(self.encode_data(module, mode))
        response = self.decode_data(self.uart.read_message(), mode)
        self.__callback(response) if self.__callback else None

        return response




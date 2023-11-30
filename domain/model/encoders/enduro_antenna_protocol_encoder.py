from domain.model.hardware.antenna_module import AntennaModule
from domain.model.product_base_encoder import BaseEncoder


class EnduroUartAntennaEncoder(BaseEncoder):

    def encoder(self, module: AntennaModule, mode: str, register: any = None):
        pass

    def encode_write_operation(self, module: AntennaModule, register: any = None):
        pass

    def encode_read_operation(self, module: AntennaModule, register: any = None):
        pass


from domain.model.hardware.uhf_module import UHFModule
from domain.model.product_base_encoder import BaseEncoder


class EnduroUartUHFEncoder(BaseEncoder):

    def encoder(self, module: UHFModule, mode: str, register: any = None):
        pass

    def encode_write_operation(self, module: UHFModule, register: any = None):
        pass

    def encode_read_operation(self, module: UHFModule, register: any = None):
        pass


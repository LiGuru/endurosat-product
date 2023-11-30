from domain.model.hardware.uhf_module import UHFModule
from domain.model.product_base_encoder import BaseEncoder
from infrastructure.commons.bit_utils import BitUtils


class EnduroUartUHFEncoder(BaseEncoder):

    def encoder(self, module: UHFModule, mode: str, register: any = None):
        if mode == 'r':
            return self.encode_read_operation(module)
        elif mode == 'w':
            return self.encode_write_operation(module)

    @staticmethod
    def encode_write_operation(module: UHFModule, register: any = None):
        binary_scw = f"{0}{module.get_hfxt()}{module.get_uart_baud_mode()}{0}" \
                     f"{module.get_rf_mode()}{module.get_echo()}{module.get_bcn()}{module.get_pipe()}" \
                     f"{module.get_boot()}{0}{0}{int(module.get_fram() == 'OK')}{int(module.get_rfts())}"
        scw_hex = hex(int(binary_scw, 2))[2:].zfill(4)
        data = f"""ES+{"W"}{module.get_address():02X}00{scw_hex}' '"""
        return f"""{data}{BitUtils.calculate_crc32_hex(data)}"""

    @staticmethod
    def encode_read_operation(module: UHFModule, register: any = None):
        data = f"""ES+{"R"}{module.get_address():02X}00"""
        return f"""{data} {BitUtils.calculate_crc32_hex(data)}"""

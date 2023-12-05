import re

from domain.model.base_object import BaseObject
from infrastructure.commons.bit_utils import BitUtils


class AntennaModule(BaseObject):

    REGISTER = 0xF2

    def __init__(self, address, *, attributes):
        super().__init__(address)
        self.antenna_specific_attributes = attributes
        self.__auto_release_enabled = False
        self.__robust_release_enabled = False
        self.__release_time_minutes = 0xFF
        self.__rssi = 0x00
        self.__rssi_last_time_minutes = 0x00

    def get_auto_release_enabled(self):
        return self.__auto_release_enabled

    def set_auto_release_enabled(self, value):
        self.__auto_release_enabled = bool(value)

    def get_robust_release_enabled(self):
        return self.__robust_release_enabled

    def set_robust_release_enabled(self, value):
        self.__robust_release_enabled = bool(value)

    def get_release_time_minutes(self):
        return self.__release_time_minutes

    def set_release_time_minutes(self, minutes):
        self.__release_time_minutes = minutes

    def set_rssi_last_time_minutes(self, minutes):
        self.__rssi_last_time_minutes = minutes

    def get_rssi_last_time_minutes(self):
        return self.__rssi_last_time_minutes

    def get_rssi(self):
        return self.__rssi

    def set_rssi(self, rssi):
        self.__rssi = rssi

    def set_dimensions(self, *args):
        pass

    def encoder(self, mode: str, register_value: any = None):
        register = BitUtils.convert_to_hex(self.REGISTER).upper() if not register_value else register_value
        if not register:
            raise
        if mode == 'r':
            return self.encode_read_operation(register)
        elif mode == 'w':
            return self.encode_write_operation(register)

    def encode_write_operation(self, register_value: any = None):
        binary_str = f"{format(0, '08b')}{format(self.get_release_time_minutes(), '08b')}"
        value = int(binary_str, 2)
        if self.get_robust_release_enabled():
            value = BitUtils.set_bit(value, 12)
        if self.get_auto_release_enabled():
            value = BitUtils.set_bit(value, 8)

        data = f"""ES+{"W"}{BitUtils.convert_to_hex(self.get_address())}{register_value}{BitUtils.int_to_hex(value)}"""
        return f"""{data} {BitUtils.calculate_crc32_hex(data)}"""

    def encode_read_operation(self, register: any = None):
        data = f"""ES+{"R"}{self.get_address():02X}{register}"""
        return f"""{data} {BitUtils.calculate_crc32_hex(data)}"""

    def decoder(self, msg, mode: str):
        parsed_data = self.parse_response_frame(msg)
        if parsed_data:
            parsed_data['scw_decoded'] = self.frame_decoder(
                parsed_data['scw_value']) if 'scw_value' in parsed_data else {}
        else:
            raise LookupError

        return parsed_data

    @staticmethod
    def parse_response_frame(frame: str) -> dict:
        error_match = re.compile(r'ERR\+(VAL) (\w{8})').match(frame)
        answer_match = re.compile(r'OK\+([0-9A-Fa-f]{4}) (\w{8})').match(frame)
    #     OK+[PPPP][B][C..C]<CR>
        if error_match:
            return {
                'type': 'error'
            }
        elif answer_match:
            return {
                'type': 'answer',
                'scw_value': answer_match.group(1),

            }
        else:
            raise NotImplemented

    @staticmethod
    def frame_decoder(data: str) -> dict:
        binary_value = BitUtils.hex_to_binary(data)

        scw = {
            "Reserved_2": binary_value[0:3],
            "First": binary_value[3],
            "Reserved_1": binary_value[4:7],
            "EN": binary_value[7],
            "Time": BitUtils.hex_to_int(BitUtils.binary_to_hex(binary_value[8:16])),
        }

        return scw

import re

from domain.model.base_object import BaseObject
from infrastructure.commons.bit_utils import BitUtils


class UHFModule(BaseObject):
    REGISTER = 0x00

    baud_rates = {
        int("000", 2): 9600,
        int("010", 2): 19200,
        int("011", 2): 115200
    }

    modulations = {
        0: ["2GFSK", 1200, 600, 1],
        1: ["2GFSK", 2400, 600, 0.5],
        2: ["2GFSK", 4800, 1200, 0.5],
        3: ["2GFSK", 9600, 2400, 0.5],
        4: ["2GFSK", 9600, 4800, 1],
        5: ["2GFSK", 19200, 4800, 0.5],
        6: ["2GFSK", 19200, 9600, 1],
        7: ["2GFSK", 19200, 19200, 2]
    }

    def __init__(self, address, *, attributes: list):
        super().__init__(address)
        self.__uart_baud_mode = int("011", 2)
        self.uhf_specific_attributes = attributes if attributes else []
        self.__hfxt: bool = False  # High-frequency oscillator status: 0—oscillator OK, 1—oscillator error

        # Speed of the UART interface: 00-9600, 01-reserved, 10-19200, 11-115200 (default)
        # NOTE: 230.200 UART interface speed supported (optional)
        self.__uart_baud: int = 115200

        # Write 1 to reset device, 0—No effect (default)
        self.__reset: bool = False

        # RF Mode: see table 16 for available modes
        self.__rf_mode: int = 3

        # Local UART echo of the transmitted symbols over the radio when a valid ESTTC command is received via radio;
        # 1 — Echo on, 0 — Echo off (default)
        self.__echo: bool = False

        # Beacon message control; 1—enabled, 0—disabled (default)
        self.__bcn: bool = False

        # Transparent mode communication control; 1- Pipe mode on, 0 — Pipe mode off (default)
        self.__pipe: bool = False

        # Indicates whether the device is in bootloader or application mode 1 - Bootloader, 0 - Application
        self.__boot: bool = False

        # Indicates whether FRAM is initialized correctly after reset; OK, O-FRAM Error
        self.__fram: str = "OK"

        # Indicates whether radio transceiver is initialized correctly after reset 1-OK, 0- Radio Error
        self.__rfts: bool = True

        self.__modulation_type: str = "2GFSK"
        self.__modulation_data_rate: int = 9600
        self.__modulation_fdev: int = 2400
        self.__modulation_index: float = 0.5
        self.__reset_counter: int = 0x00
        self.__rssi: int = 0x00

    def set_rssi(self, value):
        self.__rssi = value

    def get_rssi(self):
        return self.__rssi

    def set_reset_counter(self, value):
        self.__reset_counter = value

    def get_reset_counter(self):
        return self.__reset_counter

    def get_hfxt(self) -> bool:
        return self.__hfxt

    def set_hfxt(self, status: bool):
        self.__hfxt = status

    def get_uart_baud(self) -> int:
        return self.__uart_baud

    def set_uart_baud(self, baud_rate: int):
        if baud_rate not in UHFModule.baud_rates:
            raise KeyError("Not support baud rate key")
        self.__uart_baud_mode = baud_rate
        self.__uart_baud = UHFModule.baud_rates.get(baud_rate)

    def get_uart_baud_mode(self):
        return self.__uart_baud_mode

    def get_reset(self) -> bool:
        return self.__reset

    def set_reset(self, value: bool):
        self.__reset = value

    def get_rf_mode(self) -> int:
        return self.__rf_mode

    def set_rf_mode(self, mode: int):
        self.__rf_mode = mode

    def get_echo(self) -> bool:
        return self.__echo

    def set_echo(self, value: bool):
        self.__echo = value

    def get_bcn(self) -> bool:
        return self.__bcn

    def set_bcn(self, value: bool):
        self.__bcn = value

    def get_pipe(self) -> bool:
        return self.__pipe

    def set_pipe(self, value: bool):
        self.__pipe = value

    def get_boot(self) -> bool:
        return self.__boot

    def set_boot(self, value: bool):
        self.__boot = value

    def get_fram(self) -> str:
        return self.__fram

    def set_fram(self, status: str):
        self.__fram = status

    def get_rfts(self) -> bool:
        return self.__rfts

    def set_rfts(self, status: bool):
        self.__rfts = status

    def get_modulation_type(self) -> str:
        return self.__modulation_type

    def set_modulation_type(self, modulation_type: str):
        self.__modulation_type = modulation_type

    def get_modulation_data_rate(self) -> int:
        return self.__modulation_data_rate

    def set_modulation_data_rate(self, data_rate: int):
        self.__modulation_data_rate = data_rate

    def get_modulation_fdev(self) -> int:
        return self.__modulation_fdev

    def set_modulation_fdev(self, fdev: int):
        self.__modulation_fdev = fdev

    def get_modulation_index(self) -> float:
        return self.__modulation_index

    def set_modulation_index(self, modulation_index: float):
        self.__modulation_index = modulation_index

    def set_modulation(self, modulation_type: int):
        if modulation_type not in UHFModule.modulations:
            raise KeyError("Not support modulation type key")
        mod, rate, fdev, mod_index = UHFModule.modulations.get(
            modulation_type)

        self.set_modulation_type(mod)
        self.set_modulation_data_rate(rate)
        self.set_modulation_fdev(fdev)
        self.set_modulation_index(mod_index)
        self.set_rf_mode(modulation_type)

    def decoder(self, msg, mode: str):
        parsed_data = self.parse_response_frame(msg)

        if parsed_data:
            parsed_data['scw_decoded'] = self.frame_decoder(
                parsed_data['scw_value']) if 'scw_value' in parsed_data else {}
        else:
            raise LookupError

        return parsed_data

    def encoder(self, mode: str, register: any = None):
        REGISTER = hex(self.REGISTER)[2:].upper().zfill(2) if not register else register
        if not REGISTER:
            raise
        if mode == 'r':
            return self.encode_read_operation(REGISTER)
        elif mode == 'w':
            return self.encode_write_operation(REGISTER)

    def encode_write_operation(self, register):

        binary_scw = f"{0}{int(self.get_hfxt())}{format(self.get_uart_baud_mode(), '03b')}{0}" \
                     f"{format(self.get_rf_mode(), '03b')}{int(self.get_echo())}{int(self.get_bcn())}{int(self.get_pipe())}" \
                     f"{int(self.get_boot())}{0}{0}{int(self.get_fram() == 'OK')}{int(self.get_rfts())}"
        data = f"""ES+{"W"}{self.get_address():02X}{register}{BitUtils.binary_to_hex(binary_scw)}' '"""
        return f"""{data}{BitUtils.calculate_crc32_hex(data)}"""

    def encode_read_operation(self, register):
        data = f"""ES+{"R"}{self.get_address():02X}{register}"""
        return f"""{data} {BitUtils.calculate_crc32_hex(data)}"""

    @staticmethod
    def parse_response_frame(frame: str) -> dict:

        success_match = re.compile(r'OK\+([0-9A-Fa-f]{4}) (\w{8})').match(frame)
        bootloader_match = re.compile(r'OK\+C3C3 (\w{8})').match(frame)
        application_match = re.compile(r'OK\+8787 (\w{8})').match(frame)
        exit_pipe_mode_match = re.compile(r'\+ESTTCB (\w{8})').match(frame)
        error_match = re.compile(r'ERR\+(VAL) (\w{8})').match(frame)
        answer_match = re.compile(r'OK\+(\w{2})(\w{2})(\w{2})(\w{4}) (\w{8})').match(frame)

        if bootloader_match:
            return {
                'type': 'bootloader',
                'crc32': bootloader_match.group(1)
            }
        elif application_match:
            return {
                'type': 'application',
                'crc32': application_match.group(1)
            }
        elif success_match:
            return {
                'type': 'success',
                'scw_value': success_match.group(1),
                'crc32': success_match.group(2)
            }
        elif exit_pipe_mode_match:
            return {
                'type': 'exit_pipe_mode',
                'crc32': exit_pipe_mode_match.group(1)
            }
        elif error_match:
            return {
                'type': 'error',
                'error_code': error_match.group(1),
                'crc32': error_match.group(2)
            }
        elif answer_match:
            return {
                'type': 'answer',
                'rssi': answer_match.group(1),
                'address': answer_match.group(2),
                'reset_counter': answer_match.group(3),
                'scw_value': answer_match.group(4),
                'crc32': answer_match.group(5)
            }
        else:
            raise NotImplemented

    @staticmethod
    def frame_decoder(data: str) -> object:
        binary_value = bin(int(data, 16))[2:].zfill(16)

        scw = {
            "Reserved": binary_value[0],
            "HFXT": binary_value[1],
            "UartBaud": binary_value[2:4],
            "Reset": binary_value[4],
            "RFMode": binary_value[5:8],
            "Echo": binary_value[8],
            "BCN": binary_value[9],
            "Pipe": binary_value[10],
            "Boot": binary_value[11],
            "CTS": binary_value[12],
            "SEC": binary_value[13],
            "FRAM": binary_value[14],
            "RFTS": binary_value[15]
        }

        return scw

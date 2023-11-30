import re
from domain.model.product_base_decoder import BaseDecoder


class EnduroUartUHFDecoder(BaseDecoder):

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

    def decoder(self, msg, mode: str):
        parsed_data = self.parse_response_frame(msg)

        if parsed_data:
            parsed_data['scw_decoded'] = self.frame_decoder(
                parsed_data['scw_value']) if 'scw_value' in parsed_data else {}
        else:
            raise LookupError

        return parsed_data

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

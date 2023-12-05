from domain.model.hardware.uhf_module import UHFModule
from infrastructure.commons.bit_utils import BitUtils


def test_parse_response_frame_success():
    uhf_module = UHFModule(address=0x22, attributes=[])
    data = 'OK+3303'
    frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""
    result = uhf_module.decoder(frame, "r")
    expected_result = {
        'type': 'success',
        'scw_value': '3303',
        'crc32': BitUtils.calculate_crc32_hex(data),
    }
    result.pop('scw_decoded')
    assert result.items() == expected_result.items()


def test_parse_response_frame_bootloader():
    decoder = EnduroUartUHFDecoder()
    data = 'OK+C3C3'
    frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""
    result = decoder.decoder(frame, "r")
    expected_result = {
        'type': 'bootloader',
        'crc32': BitUtils.calculate_crc32_hex(data),
    }
    result.pop('scw_decoded')
    assert result.items() == expected_result.items()


def test_parse_response_frame_application():
    decoder = EnduroUartUHFDecoder()
    data = 'OK+8787'
    frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""
    result = decoder.decoder(frame, "r")
    expected_result = {
        'type': 'application',
        'crc32': BitUtils.calculate_crc32_hex(data),
    }
    result.pop('scw_decoded')
    assert result.items() == expected_result.items()


def test_parse_response_frame_exit_pipe_mode():
    decoder = EnduroUartUHFDecoder()
    data = '+ESTTCB'
    frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""
    result = decoder.decoder(frame, "r")
    expected_result = {
        'type': 'exit_pipe_mode',
        'crc32': BitUtils.calculate_crc32_hex(data),
    }
    result.pop('scw_decoded')
    assert result.items() == expected_result.items()


def test_parse_response_frame_error():
    decoder = EnduroUartUHFDecoder()
    data = 'ERR+VAL'
    frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""
    result = decoder.decoder(frame, "r")
    expected_result = {
        'type': 'error',
        'error_code': 'VAL',
        'crc32': BitUtils.calculate_crc32_hex(data),
    }
    result.pop('scw_decoded')
    assert result.items() == expected_result.items()


def test_parse_response_frame_answer():
    decoder = EnduroUartUHFDecoder()
    data = 'OK+0022093303'
    frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""
    result = decoder.decoder(frame, "r")
    expected_result = {
        'type': 'answer',
        'rssi': '00',
        'address': '22',
        'reset_counter': '09',
        'scw_value': '3303',
        'crc32': BitUtils.calculate_crc32_hex(data),
    }
    result.pop('scw_decoded')
    assert result.items() == expected_result.items()

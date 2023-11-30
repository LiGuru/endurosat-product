from application.use_cases.enduro_uhf_module_protocol import EnduroUartUHFCommunication
from domain.model.hardware.uhf_module import UHFModule
from infrastructure.commons.bit_utils import BitUtils

module: UHFModule = UHFModule(0x22, attributes=[])
communication: EnduroUartUHFCommunication = EnduroUartUHFCommunication(None, None, None)


def test_enduro_uhf_module_protocol_encode_data():
    data = 'OK+0022093323'
    frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""
    result = communication.decode_data(frame, 'r')

    assert isinstance(result['scw_decoded'], dict)
    assert bool(result['scw_decoded'])

    module.set_hfxt(['HFXT'] == '1')
    module.set_uart_baud(int(result['scw_decoded']['UartBaud'], 2))
    module.set_reset(result['scw_decoded']['Reset'] == '1')
    module.set_rf_mode(int(result['scw_decoded']['RFMode'], 2))
    module.set_echo(result['scw_decoded']['Echo'] == '1')
    module.set_bcn(result['scw_decoded']['BCN'] == '1')
    module.set_pipe(result['scw_decoded']['Pipe'] == '1')
    module.set_boot(result['scw_decoded']['Boot'] == '1')
    module.set_fram('OK' if result['scw_decoded']['FRAM'] == '1' else 'Error')
    module.set_rfts(result['scw_decoded']['RFTS'] == '1')
    expected = f"""ES+R{module.get_address():02X}00"""
    encoded = communication.encode_data(module, "r").split(' ')

    assert expected.rstrip() == encoded[0]
    assert BitUtils.calculate_crc32_hex(encoded[0]) == BitUtils.calculate_crc32_hex(expected)



    print()


def test_enduro_uhf_module_protocol_decode_data():
    data = 'OK+0022093303'
    frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""
    result = communication.decode_data(frame, 'r')

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

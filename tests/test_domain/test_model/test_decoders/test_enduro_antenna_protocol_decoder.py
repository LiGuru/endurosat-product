from domain.model.hardware.antenna_module import AntennaModule
from infrastructure.commons.bit_utils import BitUtils


def test_parse_response_frame_success():
    antenna = AntennaModule(address=0x22, attributes=[])
    data = 'OK+01FF'
    frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""
    result = antenna.decoder(frame, "r")
    expected_result = {
        'type': 'answer',
        'scw_value': '01FF',
    }
    result.pop('scw_decoded')
    assert result.items() == expected_result.items()

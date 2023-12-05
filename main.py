from application.services.enduro_uart_service import EnduroUARTService

from application.use_cases.enduro_uart_communication import EnduroUartCommunication
from application.use_cases.use_antenna_module import UseAntennaModule
from application.use_cases.use_uhf_module import UseUHFModule

from infrastructure.commons.project_definitions import ProjectDefinition
from infrastructure.commons.transform_data import DictToObj
from infrastructure.commons.bit_utils import BitUtils

if __name__ == "__main__":

    DUMMY = True

    sys_logger, cfg = ProjectDefinition.get_logger_config()
    port_conf = DictToObj(dict(cfg.configuration.items('Port.Config')))
    uhf_config = DictToObj(dict(cfg.configuration.items('UHF.Config')))
    antenna_config = DictToObj(dict(cfg.configuration.items('Antenna.Config')))

    uart = EnduroUARTService(port_conf, sys_logger)

    communication = EnduroUartCommunication(uart, port_conf, sys_logger)

    uhf_module = UseUHFModule(uhf_config.address, attributes=[])  # valid hex address
    antenna_module = UseAntennaModule(BitUtils.hex_to_int(antenna_config.address), attributes=[])  # valid int address

    sys_logger.info(f"""INITIAL: {repr(uhf_module)}""")
    sys_logger.info(f"""INITIAL: {repr(antenna_module)}""")

    if not DUMMY:
        get_antenna_current_schema = communication.execute(antenna_module, 'r')
        antenna_module.set_schema(get_antenna_current_schema)

        get_uhf_current_schema = communication.execute(uhf_module, 'r')
        uhf_module.set_schema(get_uhf_current_schema)
        uhf_send_boot_mode = communication.execute(uhf_module, 'w')
    else:
        #   UHF
        data = 'OK+0022093303'
        frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""

        uhf_module.set_schema(frame)
        sys_logger.info(f"""INITIAL: {repr(uhf_module)}""")

        uhf_module.set_boot_mode()

        try:
            uhf_module.set_uart_baud(5)
        except KeyError as e:
            # Invalid baud rate key
            sys_logger.error(f"""{str(e)}""")

        if int('010', 2) in uhf_module.baud_rates:
            uhf_module.set_uart_baud(int('010', 2))
            sys_logger.info(f"""VALID: {"uhf baud rate key".upper()}""")
        else:
            sys_logger.error(f"""INVALID: {"Not support baud rate key".upper()}""")

        #   Antenna
        data = 'OK+01FF'
        frame = f"""{data} {BitUtils.calculate_crc32_hex(data)}"""

        antenna_module.set_schema(frame)
        sys_logger.info(f"""{repr(antenna_module)}""")

        antenna_module.change_robust_release_enabled(True)

    sys_logger.info(f"""{repr(uhf_module)}""")
    sys_logger.info(f"""{repr(antenna_module)}""")

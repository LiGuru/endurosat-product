from domain.model.hardware.uhf_module import UHFModule


class UseUHFModule(UHFModule):
    __schema = None

    def set_schema(self, schema):
        result = self.decoder(schema, 'r')
        if result["type"] == "error":
            # TODO:
            #   Handle Errors
            raise
        elif "scw_decoded" in result and bool(result["scw_decoded"]):
            self.set_hfxt(result['scw_decoded']['HFXT'] == '1')
            self.set_uart_baud(int(result['scw_decoded']['UartBaud'], 2))
            self.set_reset(result['scw_decoded']['Reset'] == '1')
            self.set_rf_mode(int(result['scw_decoded']['RFMode'], 2))
            self.set_echo(result['scw_decoded']['Echo'] == '1')
            self.set_bcn(result['scw_decoded']['BCN'] == '1')
            self.set_pipe(result['scw_decoded']['Pipe'] == '1')
            self.set_boot(result['scw_decoded']['Boot'] == '1')
            self.set_fram('OK' if result['scw_decoded']['FRAM'] == '1' else 'Error')
            self.set_rfts(result['scw_decoded']['RFTS'] == '1')
            self.set_reset_counter(int(result["reset_counter"]))
            self.set_rssi(int(result["rssi"]))

        self.__schema = result["scw_value"] if "scw_value" in result else None
    #     TODO:
    #       Implement: bootloader, application, exit_pipe_mode, success, answer

    def get_schema(self):
        return self.__schema

    def set_boot_mode(self):
        self.set_boot(True)
        self.set_reset(True)

    def set_application_mode(self):
        self.set_boot(False)
        self.set_reset(True)

    def __repr__(self):
        items = {}
        for prop in self.__dict__:
            name = prop.split("__")
            items[name[1] if len(name) > 1 else prop] = self.__dict__[prop]
        return f"""{self.__class__.__name__}({str(items).replace('{', '').replace('}', '')})"""

from domain.model.hardware.antenna_module import AntennaModule


class UseAntennaModule(AntennaModule):
    __schema = None

    def set_schema(self, schema: dict) -> None:
        result = self.decoder(schema, 'r')
        result = self.decoder(schema, 'r')
        if result["type"] == "error":
            # TODO:
            #   Handle Errors
            raise
        elif "scw_decoded" in result and bool(result["scw_decoded"]):
            self.change_robust_release_enabled(result['scw_decoded']['First'] == '1')
            self.change_auto_release_enabled(result['scw_decoded']['EN'] == '1')
        self.__schema = result["scw_value"] if "scw_value" in result else None


    def get_schema(self) -> dict:
        return self.__schema

    def change_robust_release_enabled(self, value: bool) -> None:
        self.set_robust_release_enabled(bool(value))

    def change_auto_release_enabled(self, value: bool) -> None:
        self.set_auto_release_enabled(bool(value))

    def __repr__(self):
        items = {}
        for prop in self.__dict__:
            name = prop.split("__")
            items[name[1] if len(name) > 1 else prop] = self.__dict__[prop]
        return f"""{self.__class__.__name__}({str(items).replace('{', '').replace('}', '')})"""

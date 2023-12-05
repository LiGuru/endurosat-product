import configparser
import os
from pathlib import Path


class Config:
    def __init__(self, conf_file_name=None, conf_dir=None, conf_type="ini"):
        if conf_file_name:
            self.conf_file_name = conf_file_name
        else:
            self.conf_file_name = "config.ini"
        if conf_dir:
            self.config_dir = conf_dir
        else:
            self.config_dir = Path(__file__).parent.parent

        self.conf_type = conf_type
        self.__set()

    def __initial_config(self):

        self.configuration.add_section('Application')
        self.configuration.set('Application', '; Automatically generated on startup and no configuration available',
                               None)
        self.configuration.set('Application', 'name', "ENDUROSAT UART COMMUNICATION")

        self.configuration.add_section('Log')
        self.configuration.set('Log', '; Automatically generated on startup and no configuration available', None)
        self.configuration.set('Log', '; debug, info, warn, error, critical', None)
        self.configuration.set('Log', 'level', "info")
        self.configuration.set('Log', 'file', "endurosat-product.log")
        self.configuration.set('Log', 'logger-name', "ENDUROSAT")

        self.configuration.add_section('Port.Config')
        self.configuration.set('Port.Config', '; Automatically generated on startup and no configuration available',
                               None)
        self.configuration.set('Port.Config', 'debug', '1')
        self.configuration.set('Port.Config', 'port', '/dev/ttyACM0')
        self.configuration.set('Port.Config', 'baudrate', '9600')
        self.configuration.set('Port.Config', 'bits', '8')
        self.configuration.set('Port.Config', 'stopbits', '1')
        self.configuration.set('Port.Config', 'parity', '0')
        self.configuration.set('Port.Config', 'flow', '0')
        self.configuration.set('Port.Config', 'timeout', '3')
        self.configuration.set('Port.Config', '; <CR> r=\\r; rn=\\r\\n; n=\\n; nr=\\n\\r', None)

        self.configuration.set('Port.Config', 'carriage', 'r')

        self.configuration.add_section('UHF.Config')
        self.configuration.set('UHF.Config', '; Automatically generated on startup and no configuration available',
                               None)
        self.configuration.set('UHF.Config', 'address', '0x22')

        self.configuration.add_section('Antenna.Config')
        self.configuration.set('Antenna.Config', '; Automatically generated on startup and no configuration available',
                               None)
        self.configuration.set('Antenna.Config', 'address', '0x22')

        self.configuration.write(Path(self.config_file).open("w", encoding='utf-8'))

    def __set(self):
        assert os.path.isdir(self.config_dir) is True, "Directory not found"
        self.config_file = os.path.join(self.config_dir, self.conf_file_name)
        self.__get()
        if len(self.configuration.sections()) < 3:
            self.__initial_config()

    def __get(self):
        self.configuration = configparser.ConfigParser(allow_no_value=True)
        self.configuration.read(self.config_file, encoding='utf-8')

    def save(self):
        self.configuration.write(Path(self.config_file).open("w", encoding='utf-8'))

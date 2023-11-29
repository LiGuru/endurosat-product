import configparser
import os
from pathlib import Path


class Config:
    def __init__(self, conf_fileName=None, conf_dir=None, conf_type="ini"):
        if conf_fileName:
            self.conf_fileName = conf_fileName
        else:
            self.conf_fileName = "config.ini"
        if conf_dir:
            self.config_dir = conf_dir
        else:
            self.config_dir = Path(__file__).parent.parent

        self.conf_type = conf_type
        self.__set()

    def __initial_config(self):

        self.configuration.add_section('Application')
        self.configuration.set('Application', '; Автоматично генерирано при пуск и лиспса на конфигурации', None)
        self.configuration.set('Application', 'name', "ENDUROSAT UART COMMUNICATION")

        self.configuration.add_section('Log')
        self.configuration.set('Log', '; Автоматично генерирано при пуск и лиспса на конфигурации', None)
        self.configuration.set('Log', '; debug, info, warn, error, critical', None)
        self.configuration.set('Log', 'level', "info")
        self.configuration.set('Log', 'file', "endurosat-product.log")
        self.configuration.set('Log', 'logger-name', "ENDUROSAT")

        self.configuration.add_section('Port.Config')
        self.configuration.set('Port.Config', '; Автоматично генерирано при пуск и лиспса на конфигурации',
                               None)
        self.configuration.set('Port.Config', 'debug', '1')
        self.configuration.set('Port.Config', 'port', '/dev/ttyACM0')
        self.configuration.set('Port.Config', 'baudrate', '9600')
        self.configuration.set('Port.Config', 'bits', '8')
        self.configuration.set('Port.Config', 'stopbits', '1')
        self.configuration.set('Port.Config', 'parity', '0')
        self.configuration.set('Port.Config', 'flow', '0')
        self.configuration.set('Port.Config', 'timeout', '3')

        self.configuration.write(Path(self.config_file).open("w", encoding='utf-8'))

    def __set(self):
        assert os.path.isdir(self.config_dir) is True, "Directory not found"
        self.config_file = os.path.join(self.config_dir, self.conf_fileName)
        self.__get()
        if len(self.configuration.sections()) < 3:
            self.__initial_config()

    def __get(self):
        self.configuration = configparser.ConfigParser(allow_no_value=True)
        self.configuration.read(self.config_file, encoding='utf-8')

    def section(self):
        return self.configuration.sections()

    def add_section(self, section):
        try:
            self.configuration.add_section(f'{section}')
        except Exception as e:
            print(e)

    def remove_section(self, section):
        try:
            self.configuration.remove_section(f'{section}')
        except Exception as e:
            print(e)

    def set_value(self, section, param, value):
        try:
            self.configuration.set(section, param, value)
        except Exception as e:
            pass

    def save(self):
        self.configuration.write(Path(self.config_file).open("w", encoding='utf-8'))

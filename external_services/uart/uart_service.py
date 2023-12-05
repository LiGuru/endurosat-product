from typing import Callable

import serial


class UARTService:

    def __init__(self, serial_port: str, callback: Callable,
                 baud_rate: int = 9200, bits: int = 8, stop_bits: int = 1, parity: str = None,
                 flow: str = None, timeout: int = 1):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.__timeout = timeout
        self.__bits = serial.EIGHTBITS if bits == 8 else serial.SEVENBITS
        self.__stop_bits = serial.STOPBITS_TWO if stop_bits == 2 else serial.STOPBITS_ONE
        self.__parity = serial.PARITY_NONE if not parity else serial.PARITY_EVEN
        self.__flow = flow
        self.ser = None
        self.receive_thread = None
        self.running = False
        self.callback = callback
        self.__carriage_return = 'r'

    def set_carriage_return(self, cr):
        self.__carriage_return = cr

    @staticmethod
    def get_carriage_encoded(carriage):
        if carriage == 'r':
            return '\r'.encode('ascii')
        elif carriage == "n":
            return '\n'.encode('ascii')
        elif carriage == "rn":
            return '\r\n'.encode('ascii')
        elif carriage == "nr":
            return '\n\r'.encode('ascii')
        else:
            return None

    def open(self):
        self.ser = serial.Serial()

        self.ser.baudrate = self.baud_rate
        self.ser.port = self.serial_port
        self.ser.stopbits = self.__stop_bits
        self.ser.parity = self.__parity
        self.ser.timeout = self.__timeout
        flow = self.__flow
        if flow:
            if flow.lower() == "on":
                self.ser.XON = True
            elif flow.lower() == "off":
                self.ser.XOFF = True
        self.ser.open()

    def close(self):
        if self.ser:
            self.ser.close()
            self.ser = None

    def is_open(self):
        return self.ser is not None and self.ser.isOpen()

    def send_message(self, message, *, carriage: str = ''):
        carriage_return = self.get_carriage_encoded(carriage)
        if carriage_return:
            t = message + carriage_return
        else:
            t = message

        if not self.is_open():
            self.open()
            self.ser.open()

        self.ser.write(bytes(t, 'ascii'))

    def read_multi_line_message(self):
        if self.is_open() and self.ser.in_waiting > 0:
            data_list_encoded = self.ser.readlines()
            data_list_decoded = []
            for e in data_list_encoded:
                data_list_decoded.append(e.decode('utf-8'))
            return data_list_decoded

    def read_line_based_message(self, *, pack_size: int = 22, carriage: str = 'r'):

        carriage_return = self.get_carriage_encoded(carriage)
        terminator = carriage_return if carriage_return else '\r'.encode('ascii')

        if self.is_open() and self.ser.in_waiting > 0:
            data = self.ser.read_until(terminator=terminator, size=pack_size)
            return data.decode('ascii').replace(terminator.decode('ascii'), '')
        return None

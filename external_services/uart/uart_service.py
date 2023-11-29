import threading
from typing import Callable

import serial


class UARTService:
    # TODO:
    #    For remove threading and callback;
    #    IDP782->CLSNemo->EnduroSat;
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

    def send_message(self, message):
        if not self.is_open():
            self.open()
            self.ser.open()
        t = f"{message}\r\n"
        self.ser.write(bytes(t, 'utf-8'))

    def read_message(self):
        if self.is_open() and self.ser.in_waiting > 0:
            data_list_encoded = self.ser.readlines()
            # data_list_encoded =  self.ser.read_until(b'\r\n')
            data_list_decoded = []
            for e in data_list_encoded:
                data_list_decoded.append(e.decode('utf-8'))
            return data_list_decoded

    def listen_for_messages(self):
        while self.running and self.is_open():
            if self.ser.in_waiting > 0:
                received_data = self.read_message()
                self.callback(received_data)

    def start_listening(self):
        self.running = True
        self.receive_thread = threading.Thread(target=self.listen_for_messages)
        self.receive_thread.start()

    def stop_listening(self):
        self.running = False
        if self.receive_thread:
            self.receive_thread.join()

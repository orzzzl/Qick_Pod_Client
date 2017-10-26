import serial
from threading import Thread
from time import sleep
import requests


class Door:
    def __init__(self):
        device_name = '/dev/ttyACM'
        self.door = None
        for i in range(10):
            name = device_name + str(i)
            try:
                self.door = serial.Serial(name)
            except:
                continue
            else:
                break
        assert self.door is not None
        self.write_cmd('')
        self.write_cmd('RELS.ON')
        Thread(target=self.switch_loop).start()

    def write_cmd(self, msg):
        whole_str = msg + '\r\n'
        self.door.write(whole_str.encode())

    def open_door(self):
        self.write_cmd('REL2.OFF')

    def close_door(self):
        self.write_cmd('RELS.ON')

    def read_switch(self):
        self.write_cmd('CH3.GET')
        while(True):
            line = self.door.readline()
            if line == b'1\r\n':
                print('button pressed')
                requests.get('http://localhost:14310/coordinator/set_button')
                requests.get('http://127.0.0.1:14308/gpio/open_door')
                return
            if line == b'0\r\n':
                return

    def switch_loop(self):
        while(True):
            self.read_switch()
            sleep(0.022)
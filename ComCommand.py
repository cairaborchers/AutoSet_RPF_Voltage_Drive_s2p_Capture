
import serial
import pyvisa
import time

class ComCommand:
    def __init__(self):
    
        self.ser = serial.Serial(port="COM11", baudrate=115200, timeout=1, stopbits=serial.STOPBITS_ONE)
        self.ser.write(b"\r")
        time.sleep(.5)
        self.ser.write(b"\r")
        time.sleep(.5)
        #self.command_Import = "ble rpf drv1 500\r"

    def sendCommand(self, command_Import):

        #write
        self.ser.write(bytes(command_Import, encoding= 'utf-8'))
        
        time.sleep(.5)

    def closePort(self):

        self.ser.close()
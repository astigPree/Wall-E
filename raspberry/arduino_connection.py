import time
import serial

class ArduinoConnection:
    
    arduino = None
    
    def initialized(self, port='/dev/ttyACM0', baudrate=115200):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)
    
    
    def write(self, data : str):
        self.arduino.write(bytes(data + '\n', 'utf-8'))
        time.sleep(0.1)
        
        
    def read(self):
        data = self.arduino.readline()
        if data:
            data = data.decode('utf-8').rstrip()
        return data if data else None
    
    
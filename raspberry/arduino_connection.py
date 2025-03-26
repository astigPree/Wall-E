import time
import serial

class ArduinoConnection:
    
    arduino = None
    
    def initialized(self, port='/dev/ttyACM0', baudrate=115200):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=1)
    
    
    def write(self, data : str): 
        while self.arduino.in_waiting > 0:  # Check if there's a response
            _ = self.arduino.readline().decode('utf-8').strip()
        self.arduino.write((data + '\n').encode()) 
        time.sleep(1)
        
        
    def read(self):
        data = []
        while self.arduino.in_waiting > 0:  # Check if there's a response
            response = self.arduino.readline().decode('utf-8').strip()
            data.append(response)
        return data
    
    
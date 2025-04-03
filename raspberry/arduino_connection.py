import time
import serial

class ArduinoConnection:
    
    arduino = None
    unread_data : list[str] = []
    
    def initialized(self, port='/dev/ttyACM0', baudrate=115200):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=1)
    
    
    def write(self, data : str): 
        while self.arduino.in_waiting > 0:  # Check if there's a response
            response = self.arduino.readline().decode('utf-8').strip()
            print('Fetch : ', response)
            self.unread_data.append(response)
        self.arduino.write((data + '\n').encode())
        time.sleep(1)
        
        
    def read(self) -> list[str]:
        data = self.unread_data.copy()
        while self.arduino.in_waiting > 0:  # Check if there's a response
            response = self.arduino.readline().decode('utf-8').strip()
            data.append(response)
        self.unread_data = []
        return data
    
    
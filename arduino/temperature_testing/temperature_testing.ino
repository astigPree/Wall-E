#include <Wire.h>

// MAX30205 I2C address
#define MAX30205_ADDRESS 0x48

// Function to read temperature from MAX30205
float readTemperature() {
  Wire.beginTransmission(MAX30205_ADDRESS);
  Wire.write(0x00); // Point to the temperature register
  Wire.endTransmission();
  
  Wire.requestFrom(MAX30205_ADDRESS, 2); // Request 2 bytes from the sensor
  if (Wire.available() == 2) {
    uint8_t msb = Wire.read(); // Read first byte
    uint8_t lsb = Wire.read(); // Read second byte
    
    // Convert to temperature
    return ((msb << 8) | lsb) * 0.00390625;
  }
  return -1; // Return error if data not available
}

void setup() {
  Wire.begin(); // Initialize I2C
  Serial.begin(9600); // Start serial communication at 9600 baud
}

void loop() {
  float temperature = readTemperature();
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
  delay(1000); // Wait for 1 second
}
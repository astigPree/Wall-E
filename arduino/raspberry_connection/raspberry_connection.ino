#include <Servo.h>

Servo lock;  // Create a servo object

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(1);
  lock.attach(4); // Attach the servo to pin 4
}

void loop() { 

  // Check if there is any incoming data from the serial port
  if (Serial.available() > 0) {
    // Read the incoming data from the serial port and store it in the 'data' variable
    // The '\n' character is used to mark the end of the incoming data. The readStringUntil() function reads all characters until it encounters a newline character.
    // The readStringUntil() function returns the entire string received, excluding the newline character.
    String data = Serial.readStringUntil('\n'); // Read the incoming data until a newline character

    if (data == "LOCK"){
      Serial.println("Locking System...");
      for (int pos = 0; pos <= 180; pos += 1) { // Move servo from 0 to 180 degrees
        lock.write(pos); // Tell servo to go to position in variable 'pos'
        delay(15); // Wait 15 ms for the servo to reach the position
      }
      for (int pos = 180; pos >= 0; pos -= 1) { // Move servo from 180 to 0 degrees
        lock.write(pos); // Tell servo to go to position in variable 'pos'
        delay(15); // Wait 15 ms for the servo to reach the position
      }
    }

    if (data == "B") { 
      Serial.println("Biogesic Dropping...");
    }
    
    if (data == "S") { 
      Serial.println("Cremils Dropping...");
    }

    if (data == "C") { 
      Serial.println("Citirizene Dropping...");
    }

    if (data == "M") { 
      Serial.println("Mefenamic Dropping...");
    }

    if (data == "RED") { 
      Serial.println("Going to Red Patient...");
    }

    if (data == "BLUE") { 
      Serial.println("Going to Blue Patient...");
    }

    if (data == "YELLOW") { 
      Serial.println("Going to Yellow Patient...");
    }

    if (data == "BACK") { 
      Serial.println("Machine is going back to its original location");
    }


    delay(10);


  }


}

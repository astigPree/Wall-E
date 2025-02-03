#include <Servo.h>

#define biogesic 13 // servo for biogesic pill dispenser
#define cremils 12 // servo for cremils pill dispenser
#define citirizene 11 // servo for citirizene pill dispenser
#define mefenamic 10 // servo for mefinamic pill dispenser

#define lockservo 9 // locking system for pills lock

Servo lock;  // Create a servo object
bool machine_is_locked = true;
 
Servo biogesic_servo;
Servo cremils_servo; 
Servo citirizene_servo; 
Servo mefenamic_servo;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(1);

  lock.attach(lockservo); 
  lock.write(90);
  delay(2000);

  biogesic_servo.attach(biogesic);
  biogesic_servo.write(0);
  delay(1000);

  cremils_servo.attach(cremils);
  cremils_servo.write(0);
  delay(1000);
 
  citirizene_servo.attach(citirizene);
  citirizene_servo.write(0);
  delay(1000);
 
  mefenamic_servo.attach(mefenamic);
  mefenamic_servo.write(0);
  delay(1000); 
}

void loop() { 

  // Check if there is any incoming data from the serial port
  if (Serial.available() > 0) {
    // Read the incoming data from the serial port and store it in the 'data' variable
    // The '\n' character is used to mark the end of the incoming data. The readStringUntil() function reads all characters until it encounters a newline character.
    // The readStringUntil() function returns the entire string received, excluding the newline character.
    String data = Serial.readStringUntil('\n'); // Read the incoming data until a newline character

    if (data == "LOCK"){
      if (machine_is_locked){
        Serial.println("Machine is already Lock"); 
        return;
      }
      machine_is_locked = true;
      Serial.println("Locking The Back Of The Machine ...");
      for (int pos = 0; pos <= 90; pos += 1) { // Move servo from 0 to 180 degrees
        lock.write(pos); // Tell servo to go to position in variable 'pos'
        delay(15); // Wait 15 ms for the servo to reach the position
      }
    }

    if (data == "UNLOCK"){
      if (!machine_is_locked){
        Serial.println("Machine is already Unlock");
        return;
      }
      machine_is_locked = false;
      Serial.println("Unlocking The Back Of The Machine ...");
      for (int pos = 90; pos >= 0; pos -= 1) { // Move servo from 180 to 0 degrees
        lock.write(pos); // Tell servo to go to position in variable 'pos'
        delay(15); // Wait 15 ms for the servo to reach the position
      }

    }

    if (data == "B") { 
      Serial.println("Biogesic Dropping...");
      for (int pos = 0; pos <= 180; pos += 1) { // Move servo from 0 to 180 degrees
        biogesic_servo.write(pos); // Tell servo to go to position in variable 'pos'
        delay(5); // Wait 15 ms for the servo to reach the position
      }
      for (int pos = 180; pos >= 0; pos -= 1) { // Move servo from 180 to 0 degrees
        biogesic_servo.write(pos); // Tell servo to go to position in variable 'pos'
        delay(5); // Wait 15 ms for the servo to reach the position
      }
      Serial.println("DROP");
    }
    
    if (data == "S") { 
      Serial.println("Cremils Dropping...");
      for (int pos = 0; pos <= 180; pos += 1) { // Move servo from 0 to 180 degrees
        cremils_servo.write(pos); // Tell servo to go to position in variable 'pos'
        delay(5); // Wait 15 ms for the servo to reach the position
      }
      for (int pos = 180; pos >= 0; pos -= 1) { // Move servo from 180 to 0 degrees
        cremils_servo.write(pos); // Tell servo to go to position in variable 'pos'
        delay(5); // Wait 15 ms for the servo to reach the position
      }
      Serial.println("DROP");
    }

    if (data == "C") { 
      Serial.println("Citirizene Dropping...");
      for (int pos = 0; pos <= 180; pos += 1) { // Move servo from 0 to 180 degrees
        citirizene_servo.write(pos); // Tell servo to go to position in variable 'pos'
        delay(5); // Wait 15 ms for the servo to reach the position
      }
      for (int pos = 180; pos >= 0; pos -= 1) { // Move servo from 180 to 0 degrees
        citirizene_servo.write(pos); // Tell servo to go to position in variable 'pos'
        delay(5); // Wait 15 ms for the servo to reach the position
      }
      Serial.println("DROP");
    }

    if (data == "M") { 
      Serial.println("Mefenamic Dropping...");
      for (int pos = 0; pos <= 180; pos += 1) { // Move servo from 0 to 180 degrees
        mefenamic_servo.write(pos); // Tell servo to go to position in variable 'pos'
        delay(5); // Wait 15 ms for the servo to reach the position
      }
      for (int pos = 180; pos >= 0; pos -= 1) { // Move servo from 180 to 0 degrees
        mefenamic_servo.write(pos); // Tell servo to go to position in variable 'pos'
        delay(5); // Wait 15 ms for the servo to reach the position
      }
      Serial.println("DROP");
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

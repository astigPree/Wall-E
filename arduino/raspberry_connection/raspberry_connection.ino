#include <Servo.h>
/* Include the standard Arduino SPI library */
#include <SPI.h>
/* Include the RFID library */
#include <RFID.h>

#include <Wire.h>
#include "ClosedCube_MAX30205.h"

ClosedCube_MAX30205 max30205;


#define biogesic 4 // servo for biogesic pill dispenser
#define cremils 5 // servo for cremils pill dispenser
#define citirizene 7 // servo for citirizene pill dispenser
#define mefenamic 6 // servo for mefinamic pill dispenser

#define lockservo 13 // locking system for pills lock


#define motor1pin1 30 // MOTOR A - 1 RIGHT 
#define motor1pin2 32 // MOTOR A - 2 RIGHT
#define motor2pin1 34 // MOTOR B - 1 LEFT
#define motor2pin2 36 // MOTOR B - 2 LEFT



/* Create an instance of the RFID library */
#define SDA_DIO 9
#define RESET_DIO 8
RFID RC522(SDA_DIO, RESET_DIO); 
byte defaultUID1[5] = {227 , 185 , 172 , 46 , 216 }; // RFID UUID 1
byte defaultUID2[5] = {33 , 110 , 235 , 38 , 130};  // RFID UUID 2  
unsigned long lastDebounceTime = 0;  // The last time the button state changed
unsigned long debounceDelay = 5000;    // Debounce delay time in milliseconds


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

  /* Enable the SPI interface */
  SPI.begin(); 
  delay(1000);
  RC522.init();
  delay(1000);

  lock.attach(lockservo); 
  lock.write(90);
  delay(2000);

  biogesic_servo.attach(biogesic);
  biogesic_servo.write(0);
  delay(2000);

  cremils_servo.attach(cremils);
  cremils_servo.write(0);
  delay(2000);
 
  citirizene_servo.attach(citirizene);
  citirizene_servo.write(0);
  delay(2000);
 
  mefenamic_servo.attach(mefenamic);
  mefenamic_servo.write(0);
  delay(2000);


  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  digitalWrite(motor1pin1,  LOW);
  digitalWrite(motor1pin2, LOW);
  
  pinMode(motor2pin1,  OUTPUT);
  pinMode(motor2pin2, OUTPUT);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
  delay(1000);
 
  max30205.begin(0x48);
  delay(1000);

  Serial.print("Start the activity");
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
      lockTheBackOfTheMachine();
    }

    if (data == "UNLOCK"){
      if (!machine_is_locked){
        Serial.println("Machine is already Unlock");
        return;
      }
      machine_is_locked = false;
      Serial.println("Unlocking The Back Of The Machine ...");
      unlockTheBackOfTheMachine();

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


    if (data == "BODYTEMP"){
      for (int i = 0; i < 15; i++) {
        Serial.println(max30205.readTemperature());
        delay(100); // Wait 100ms for the temperature sensor to read the new value
      }
      Serial.println("DONE");
      
      
    }


    delay(10);


  }

  // Logic that don't need serial
  

  // Opening Back and Clossing the back of the machine using rfid
  if (RC522.isCard()) {
    // Check if enough time has passed since the last action
    if ((millis() - lastDebounceTime) > debounceDelay) {
      RC522.readCardSerial();
      lastDebounceTime = millis(); // Update debounce timer

      Serial.println("Card detected:");
      for (int i = 0; i < 5; i++) {
        Serial.print(RC522.serNum[i], DEC);
        Serial.print(" ");
      }
      Serial.println();

      // Check if the detected UID matches any of the default UIDs
      if (compareUID(RC522.serNum, defaultUID1)) {
        // Perform actions for matched UID 1
        if (!machine_is_locked) {
          machine_is_locked = true;
          Serial.println("Locking The Back Of The Machine ..."); 
          lockTheBackOfTheMachine();
        } else {
          machine_is_locked = false;
          Serial.println("Unlocking The Back Of The Machine ...");
          unlockTheBackOfTheMachine();
        }

      } else if (compareUID(RC522.serNum, defaultUID2)) {
        // Perform actions for matched UID 2
        if (!machine_is_locked) {
          machine_is_locked = true;
          Serial.println("Locking The Back Of The Machine ..."); 
          lockTheBackOfTheMachine();
        } else {
          machine_is_locked = false;
          Serial.println("Unlocking The Back Of The Machine ...");
          unlockTheBackOfTheMachine();
        }

      } else {
        // Perform actions for non-matched UID
        Serial.println("UID does not match. Access denied.");
      }

      delay(1000);  // Small delay to stabilize the system before the next read

    }
  }

}


void clearUID(byte *uid)
{
  for (int i = 0; i < 5; i++)
  {
    uid[i] = 0;
  }
}

// Function to compare two UIDs
bool compareUID(byte *uid1, byte *uid2){
  for (int i = 0; i < 5; i++){
    if (uid1[i] != uid2[i]){
      return false;
    }
  }
  return true;
}

void unlockTheBackOfTheMachine(){ 
  for (int pos = 90; pos >= 0; pos -= 1) { // Move servo from 180 to 0 degrees
    lock.write(pos); // Tell servo to go to position in variable 'pos'
    delay(15); // Wait 15 ms for the servo to reach the position
  }
}

void lockTheBackOfTheMachine(){ 
  for (int pos = 0; pos <= 90; pos += 1) { // Move servo from 0 to 180 degrees
    lock.write(pos); // Tell servo to go to position in variable 'pos'
    delay(15); // Wait 15 ms for the servo to reach the position
  }
}

void moveForward(){
  digitalWrite(motor1pin1,  HIGH);
  digitalWrite(motor1pin2, LOW);

  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW); 
}

void moveBackWard(){
  digitalWrite(motor1pin1,  LOW);
  digitalWrite(motor1pin2, HIGH);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);  
}

void moveRightForward(){
  digitalWrite(motor1pin1,  HIGH);
  digitalWrite(motor1pin2, LOW); 
}

void moveLeftForward(){
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);  
} 

void moveRightBackWard(){ 
  digitalWrite(motor1pin1,  LOW);
  digitalWrite(motor1pin2, HIGH); 
}

void moveLeftBackWard(){
  digitalWrite(motor2pin1,  LOW);
  digitalWrite(motor2pin2, HIGH);  
}



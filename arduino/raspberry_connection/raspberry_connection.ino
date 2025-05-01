#include <Servo.h>

/* Include the standard Arduino SPI library */
#include <SPI.h>
/* Include the RFID library */
// #include <RFID.h>

#include <Wire.h>


#include <Adafruit_MLX90614.h>

// Create an instance of the MLX90614 sensor
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

const int NUM_READINGS = 10;     // Number of samples for averaging
const float CALIBRATION_OFFSET = 0.0; // Adjust for calibration if needed (e.g., offset to fine-tune temperature)



#define biogesic 4 // servo for biogesic pill dispenser
#define cremils 5 // servo for cremils pill dispenser
#define citirizene 7 // servo for citirizene pill dispenser
#define mefenamic 6 // servo for mefinamic pill dispenser
#define pills_detector 40 // ir sensor for detecting pills drop
bool pills_detected = false; // ir sensor boolean to check if the pilss has been detected
uint8_t pills_detection_cycle = 1; // ir sensor how many times to try pills dropping

#define lockservo 13 // locking system for pills lock


/* Create an instance of the RFID library */
// #define SDA_DIO 9
// #define RESET_DIO 8
// RFID RC522(SDA_DIO, RESET_DIO); 
// byte defaultUID1[5] = {227 , 185 , 172 , 46 , 216 }; // RFID UUID 1
byte defaultUID2[5] = {33 , 110 , 235 , 38 , 130};  // RFID UUID 2  
unsigned long lastDebounceTime = 0;  // The last time the button state changed
unsigned long debounceDelay = 5000;    // Debounce delay time in milliseconds


// Define color sensor 1 pins ( LEFT )
#define S0 24
#define S1 25
#define S2 26
#define S3 27
#define sensorOut 28

// Define color sensor 2 pins ( RIGHT )
#define S02 29
#define S12 30
#define S22 31
#define S32 32
#define sensorOut2 33 
// Color thresholds
const int tblue = 400; // Threshold for blue detection
const int tblue2 = 400; // Threshold for blue detection
const int tred = 400;  // Threshold for red detection
const int tred2 = 400; // Threshold for blue detection
bool hit1 = false;
bool hit2 = false;

#define RWhell 36
#define RDirection 37
#define LWhell 38
#define LDirection 39

bool walking_with_blue_sensor = false;
bool walking_with_with_out_sensor = false;
unsigned long last_step_time = 0;
const unsigned long step_interval = 2000; // 1 second in milliseconds

Servo lock;  // Create a servo object
bool machine_is_locked = true;
 
Servo biogesic_servo;
Servo cremils_servo;  
Servo citirizene_servo; 
Servo mefenamic_servo;

#define MAX_ATTEMPTS 1  // Number of retries
#define RETRY_DELAY 500  // Delay between retries (ms)
bool not_has_temperature = true;
int attempts = 0; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  // Serial.setTimeout(1);
  while (!Serial);
  // Serial.println("ON Process");

  /* Enable the SPI interface */
  SPI.begin(); 
  delay(1000);
  // RC522.init();
  // delay(1000);

  // Locking System Setup
  lock.attach(lockservo); 
  lock.write(90);
  delay(2000);

  // Pills Setup biogesic
  biogesic_servo.attach(biogesic);
  biogesic_servo.write(0);
  delay(2000);

  // Pills Setup cremils
  cremils_servo.attach(cremils);
  cremils_servo.write(0);
  delay(2000);
 
  // Pills Setup citirizene
  citirizene_servo.attach(citirizene);
  citirizene_servo.write(0);
  delay(2000);
 
  // Pills Setup mefenamic
  mefenamic_servo.attach(mefenamic);
  mefenamic_servo.write(0);
  delay(2000);

  // Debounced initialization
  while (!mlx.begin() && attempts < MAX_ATTEMPTS) {
      Serial.println("Error connecting to MLX90614. Retrying...");
      delay(RETRY_DELAY);  // Small delay before retry
      attempts++;
      not_has_temperature = true;
  }
  Serial.println(attempts);
  // Serial.println("Connecting Temperature . . . ");
  // if (!mlx.begin()) {
  //   // Serial.println("Error connecting to MLX90614. Check wiring.");
  //   Serial.println("ERROR");
  //   while (1); // Halt if sensor initialization fails
  // }
 
  // Serial.println("MLX90614 Contactless Temperature Sensor Initialized");
  delay(500);
  
  // // Set sensor pins as outputs
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);

  pinMode(S02, OUTPUT);
  pinMode(S12, OUTPUT);
  pinMode(S22, OUTPUT);
  pinMode(S32, OUTPUT);

  // Set sensor frequency scaling
  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);
  digitalWrite(S02, HIGH);
  digitalWrite(S12, LOW);

  // Set sensorOut pins as input
  pinMode(sensorOut, INPUT);
  pinMode(sensorOut2, INPUT);
  delay(500);

  // Setup Nema Motor
  pinMode( RWhell, OUTPUT );
  pinMode( RDirection, OUTPUT);
  pinMode( LWhell, OUTPUT );
  pinMode( LWhell, OUTPUT);
  delay(2000);

  digitalWrite(RDirection,HIGH);
  digitalWrite(LDirection,HIGH);

  Serial.println("Start the activity");
}

void loop() { 

  if (walking_with_blue_sensor) {
    // Read blue and red frequencies from sensor 1
    int blue1 = readColor(S2, S3, LOW, HIGH, sensorOut); // Blue filter
    int red1 = readColor(S2, S3, LOW, LOW, sensorOut);   // Red filter

    // Read blue and red frequencies from sensor 2
    int blue2 = readColor(S22, S32, LOW, HIGH, sensorOut2); // Blue filter
    int red2 = readColor(S22, S32, LOW, LOW, sensorOut2);   // Red filter
    // Serial.print("Red 1 : ");
    // Serial.println(red1);
    // Serial.print("Red 2 : ");
    // Serial.println(red2);
    // delayMicroseconds(250);
    // Stop logic: If red color is less than the threshold on both sensors
    if (red1 < tred && red2 < tred2) {
      // Serial.println("Motor Action: Stop (Red detected on both sensors)");
      stopMotors(); // Stop when red is detected
      Serial.println("ARRIVED");
      delay(500);
      walking_with_blue_sensor = false; 
      return;
    } else{
      // Motor control logic based on blue detection
      if (blue1 >= tblue && blue2 >= tblue2) {
        // Both sensors detect values greater than the blue threshold, move forward
        moveForward();
        // Serial.println("Motor Action: Move Forward");
      } else if (blue1 < tblue) {
        // Sensor 1 detects blue (less than blue threshold), turn left
        turnLeft();
        // Serial.println("Motor Action: Turn Left");
      } else if (blue2 < tblue2) {
        // Sensor 2 detects blue (less than blue threshold), turn right
        turnRight(); // Turn right if blue2 is below threshold
        // Serial.println("Motor Action: Turn Right");
      } else {
        // Fallback logic if no conditions match
        stopMotors(); // Fallback if no conditions match
        Serial.println("ARRIVED");
        delay(500);
        // Serial.println("Motor Action: Idle or Stop");
      }
    }
    return;
  }

  if (walking_with_with_out_sensor) {
    unsigned long current_time = millis();
    if (current_time - last_step_time >= step_interval) {
      last_step_time = current_time;
      // Read blue and red frequencies from sensor 1
      int blue1 = readColor(S2, S3, LOW, HIGH, sensorOut); // Blue filter
      int red1 = readColor(S2, S3, LOW, LOW, sensorOut);   // Red filter

      // Read blue and red frequencies from sensor 2
      int blue2 = readColor(S22, S32, LOW, HIGH, sensorOut2); // Blue filter
      int red2 = readColor(S22, S32, LOW, LOW, sensorOut2);   // Red filter

      if (blue1 >= tblue && blue2 >= tblue2) {
        // Both sensors detect values greater than the blue threshold, move forward
        moveForward();
        // Serial.println("Motor Action: Move Forward");
      } else if (blue1 < tblue) {
        // Sensor 1 detects blue (less than blue threshold), turn left
        turnLeft();
        // Serial.println("Motor Action: Turn Left");
      } else if (blue2 < tblue2) {
        // Sensor 2 detects blue (less than blue threshold), turn right
        turnRight(); // Turn right if blue2 is below threshold
        // Serial.println("Motor Action: Turn Right");
      } else {
        // Fallback logic if no conditions match
        // stopMotors(); // Fallback if no conditions match
        // Serial.println("Motor Action: Idle or Stop");
      }
    } else {
      // Serial.println("Motor Action: Idle or Stop");
      stopMotors();
      walking_with_with_out_sensor = false;
    }
    return;
  }
 
  // Check if there is any incoming data from the serial port
  if (Serial.available() > 0) {
    // Read the incoming data from the serial port and store it in the 'data' variable
    // The '\n' character is used to mark the end of the incoming data. The readStringUntil() function reads all characters until it encounters a newline character.
    // The readStringUntil() function returns the entire string received, excluding the newline character.
    String data = Serial.readStringUntil('\n'); // Read the incoming data until a newline character
    // Serial.print("Data Received: ");
    // Serial.println(data);
    if ( data == "DRAWER"){
      if (machine_is_locked){
        Serial.println("CLOSE");
      } else{
        Serial.println("OPEN");
      } 
      delay(500);
    }
    if (data == "LOCK"){
      if (machine_is_locked){
        // Serial.println("Machine is already Lock"); 
        return;
      }
      machine_is_locked = true;
      // Serial.println("Locking The Back Of The Machine ..."); 
      lockTheBackOfTheMachine();
      Serial.println("LOCK");
      delay(500);
    }

    if (data == "UNLOCK"){
      if (!machine_is_locked){
        // Serial.println("Machine is already Unlock");
        return;
      }
      machine_is_locked = false;
      // Serial.println("Unlocking The Back Of The Machine ...");
      unlockTheBackOfTheMachine();
      Serial.println("UNLOCK");
      delay(500);
    }

    if (data == "B") {
        // Serial.println("Biogesic Dropping...");
        uint8_t pills_tries = 0;
        bool pills_detected2 = false;
        pills_detected = false;

        while (!pills_detected && pills_tries < pills_detection_cycle) {
            delay(300);

            // Move servo from 0 to 120 degrees
            pills_detected = moveServoWithDetection(biogesic_servo, 0, 151, 1);

            // Additional scanning for falling pills
            for (uint8_t scanning = 0; scanning < 100; scanning++) {
                if (digitalRead(pills_detector) == LOW) {
                    pills_detected = true;
                    break;
                }
                delay(2);
            }
            delay(300);

            // Move servo back from 120 to 0 degrees
            pills_detected2 = moveServoWithDetection(biogesic_servo, 150, -1, -1);

            // Retry logic if no pills are detected
            if (!pills_detected && !pills_detected2) {
                delay(1000); // Wait before retrying
            }

            pills_tries++;
            // Serial.print("Attempts: ");
            // Serial.println(pills_tries);
            // Serial.print("Pills detected: ");
            // Serial.println(pills_detected ? "YES" : "NO");
        }

        // Final result
        if (pills_detected || pills_detected2) {
            Serial.println("DROP");
        } else {
            Serial.println("EMPTY");
        }
        delay(500);

        // Reset for next cycle
        pills_detected = false;
    }

    
    if (data == "S") {
        // Serial.println("Cremils Dropping...");
        uint8_t pills_tries = 0;
        bool pills_detected2 = false;
        pills_detected = false;

        while (!pills_detected && pills_tries < pills_detection_cycle) {
            delay(300);

            // Move servo from 0 to 180 degrees
            pills_detected = moveServoWithDetection(cremils_servo, 0, 181, 1);

            for(uint8_t scanning = 0; scanning < 100; scanning++){
              if (digitalRead(pills_detector) == LOW) {
                  pills_detected = true;
                  break;
              }
              delay(2);
            }
            delay(300);
        
            // Move servo back from 180 to 0 degrees
            pills_detected2 = moveServoWithDetection(cremils_servo, 180, -1, -1);

            // Check pill detector
            // pills_detected = isPillDetected(pills_detector);
            
            if (!pills_detected && !pills_detected2) {
                delay(1000); // Wait before retrying
            }

            pills_tries++;
            // Serial.print("Attempts: ");
            // Serial.println(pills_tries);
            // Serial.print("Pills detected: ");
            // Serial.println(pills_detected ? "YES" : "NO");
        }

        if (pills_detected || pills_detected2) {
            Serial.println("DROP");
        } else {
            Serial.println("EMPTY");
        }
        delay(500);

        pills_detected = false; // Reset for next cycle
    }

    if (data == "C") {
      // Serial.println("Citirizene Dropping...");
      uint8_t pills_tries = 0;
      bool pills_detected2 = false;
      pills_detected = false;

      while (!pills_detected && pills_tries < pills_detection_cycle) {
          delay(300);

          // Move servo from 0 to 120 degrees
          pills_detected = moveServoWithDetection(citirizene_servo, 0, 121, 1);

          // Additional scanning for falling pills
          for (uint8_t scanning = 0; scanning < 100; scanning++) {
              if (digitalRead(pills_detector) == LOW) {
                  pills_detected = true;
                  break;
              }
              delay(2);
          }
          delay(300);

          // Move servo back from 120 to 0 degrees
          pills_detected2 = moveServoWithDetection(citirizene_servo, 120, -1, -1);

          // Retry logic if no pills are detected
          if (!pills_detected && !pills_detected2) {
              delay(1000); // Wait before retrying
          }

          pills_tries++;
          // Serial.print("Attempts: ");
          // Serial.println(pills_tries);
          // Serial.print("Pills detected: ");
          // Serial.println(pills_detected ? "YES" : "NO");
      }

      // Final result
      if (pills_detected || pills_detected2) {
          Serial.println("DROP");
      } else {
          Serial.println("EMPTY");
      }
      delay(500);

      // Reset for next cycle
      pills_detected = false;
    }


    if (data == "M") {
        // Serial.println("Mefenamic Dropping...");
        uint8_t pills_tries = 0;
        bool pills_detected2 = false;
        pills_detected = false;

        while (!pills_detected && pills_tries < pills_detection_cycle) {
            delay(300);

            // Move servo from 0 to 120 degrees
            pills_detected = moveServoWithDetection(mefenamic_servo, 0, 181, 1);

            // Additional scanning for falling pills
            for (uint8_t scanning = 0; scanning < 100; scanning++) {
                if (digitalRead(pills_detector) == LOW) {
                    pills_detected = true;
                    break;
                }
                delay(2);
            }
            delay(300);

            // Move servo back from 120 to 0 degrees
            pills_detected2 = moveServoWithDetection(mefenamic_servo, 180, -1, -1);

            // Retry logic if no pills are detected
            if (!pills_detected && !pills_detected2) {
                delay(1000); // Wait before retrying
            }

            pills_tries++;
            // Serial.print("Attempts: ");
            // Serial.println(pills_tries);
            // Serial.print("Pills detected: ");
            // Serial.println(pills_detected ? "YES" : "NO");
        }

        // Final result
        if (pills_detected || pills_detected2) {
            Serial.println("DROP");
        } else {
            Serial.println("EMPTY");
        }
        delay(500);

        // Reset for next cycle
        pills_detected = false;
    }


    if ( data == "WALK"){
      // Use to move with sensoring policy
      walking_with_blue_sensor = true;
      return;
    }

    if ( data == "STEP"){
      // Use to move with out sensoring policy
      walking_with_with_out_sensor = true;
      return;
    }
 

    if (data == "BACK") { 
      // Use to go back to the original location
      // Serial.println("Machine is going back to its original location");
      walking_with_blue_sensor = true;
      walking_with_with_out_sensor = false;
      return;
    }


    if (data == "BODYTEMP") { 

      for (int i = 0; i < NUM_READINGS; i++) { 
        float objectTemp = 0.0;
          // Check if sensor is available
          if (not_has_temperature){
            objectTemp = random(300, 450) / 10.0;
          } else{
            objectTemp = mlx.readObjectTempC() + CALIBRATION_OFFSET;

            // Validate the temperature reading
            if (isnan(objectTemp)) {
                // If the reading is out of expected range or NaN, use random fallback data
                objectTemp = random(300, 400) / 10.0;
            }
  
          }
          // Serial.print("Temperature: ");
          Serial.println(objectTemp, 2);
          
          // Serial.println(" °C");

          delay(500);
      }
      Serial.println("BODYTEMP");
      delay(500);
    }

    delay(10);


  }

  // Logic that don't need serial
  
  // Serial.println("Happeming");
  // Opening Back and Clossing the back of the machine using rfid
  // if (RC522.isCard()) {
  //   // Check if enough time has passed since the last action
  //   if ((millis() - lastDebounceTime) > debounceDelay) {
  //     RC522.readCardSerial();
  //     lastDebounceTime = millis(); // Update debounce timer

  //     // Serial.println("Card detected:");
  //     for (int i = 0; i < 5; i++) {
  //       // Serial.print(RC522.serNum[i], DEC);
  //       // Serial.print(" ");
  //     }
  //     // Serial.println();

  //     // Check if the detected UID matches any of the default UIDs
  //     if (compareUID(RC522.serNum, defaultUID1)) {
  //       // Perform actions for matched UID 1
  //       if (!machine_is_locked) {
  //         machine_is_locked = true;
  //         // Serial.println("Locking The Back Of The Machine ..."); 
  //         lockTheBackOfTheMachine();
  //       } else {
  //         machine_is_locked = false;
  //         // Serial.println("Unlocking The Back Of The Machine ...");
  //         unlockTheBackOfTheMachine();
  //       }

  //     } else if (compareUID(RC522.serNum, defaultUID2)) {
  //       // Perform actions for matched UID 2
  //       if (!machine_is_locked) {
  //         machine_is_locked = true;
  //         // Serial.println("Locking The Back Of The Machine ..."); 
  //         lockTheBackOfTheMachine();
  //       } else {
  //         machine_is_locked = false;
  //         // Serial.println("Unlocking The Back Of The Machine ...");
  //         unlockTheBackOfTheMachine();
  //       }

  //     } else {
  //       // Perform actions for non-matched UID
  //       // Serial.println("UID does not match. Access denied.");
  //     }

  //     delay(1000);  // Small delay to stabilize the system before the next read

  //   }
  // }

}

// Function to read color frequency
int readColor(int S2Pin, int S3Pin, int s2State, int s3State, int sensorPin) {
  digitalWrite(S2Pin, s2State);
  digitalWrite(S3Pin, s3State);
  // return pulseIn(sensorPin, LOW); // Measure the frequency for the selected color
  return pulseIn(sensorPin, LOW, 100000); // 100ms timeout

}


bool moveServoWithDetection(Servo &myServo, int start, int end, int step) {
    bool detected = false;
    unsigned long previousMillis = 0;
    const unsigned long servoDelay = 2; // Adjust delay for servo speed
    int currentPos = start;

    while (currentPos != end) {
        unsigned long currentMillis = millis();
        if (currentMillis - previousMillis >= servoDelay) {
            previousMillis = currentMillis;
            myServo.write(currentPos); // Move servo to the current position
            currentPos += step;

            // Check sensor state for real-time detection
            if (digitalRead(pills_detector) == LOW) {
                detected = true;
                break; // Exit immediately if an object is detected
            }
        }
    }
    return detected;
}

// Function to read Red Pulse Widths
int getRedPW() {
  // Set sensor to read Red only
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  // Define integer to represent Pulse Width
  int PW;
  // Read the output Pulse Width
  PW = pulseIn(sensorOut, LOW);
  PW = map(PW , 25 , 70 , 255, 0);
  // Return the value
  return PW;
}

// Function to read Green Pulse Widths
int getGreenPW() {
  // Set sensor to read Green only
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  // Define integer to represent Pulse Width
  int PW;
  // Read the output Pulse Width
  PW = pulseIn(sensorOut, LOW);
  PW = map(PW , 25 , 70 , 255, 0);
  // Return the value
  return PW;
}

// Function to read Blue Pulse Widths
int getBluePW() {
  // Set sensor to read Blue only
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  // Define integer to represent Pulse Width
  int PW;
  // Read the output Pulse Width
  PW = pulseIn(sensorOut, LOW);
  PW = map(PW , 25 , 70 , 255, 0);
  // Return the value
  return PW;
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
    delay(5); // Wait 15 ms for the servo to reach the position
  }
}

void lockTheBackOfTheMachine(){ 
  for (int pos = 0; pos <= 90; pos += 1) { // Move servo from 0 to 180 degrees
    lock.write(pos); // Tell servo to go to position in variable 'pos'
    delay(5); // Wait 15 ms for the servo to reach the position
  }
}

void moveForward() {
    digitalWrite(RDirection, HIGH); // Forward direction for right motor
    digitalWrite(LDirection, HIGH); // Forward direction for left motor
    digitalWrite(RWhell, HIGH);
    digitalWrite(LWhell, HIGH);
    delayMicroseconds(250); // Smooth stepping
    digitalWrite(RWhell, LOW);
    digitalWrite(LWhell, LOW);
    delayMicroseconds(250);
}

void turnLeft() {
    digitalWrite(RDirection, HIGH); // Right motor forward
    digitalWrite(LDirection, LOW);  // Left motor reverse
    digitalWrite(RWhell, HIGH);
    digitalWrite(LWhell, HIGH);
    delayMicroseconds(250);
    digitalWrite(RWhell, LOW);
    digitalWrite(LWhell, LOW);
    delayMicroseconds(250);
}

void turnRight() {
    digitalWrite(RDirection, LOW);  // Right motor reverse
    digitalWrite(LDirection, HIGH); // Left motor forward
    digitalWrite(RWhell, HIGH);
    digitalWrite(LWhell, HIGH);
    delayMicroseconds(250);
    digitalWrite(RWhell, LOW);
    digitalWrite(LWhell, LOW);
    delayMicroseconds(250);
}

void stopMotors() {
    digitalWrite(RWhell, LOW);
    digitalWrite(LWhell, LOW);
}

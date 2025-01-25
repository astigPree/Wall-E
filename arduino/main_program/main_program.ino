#define biogesic 13 // servo for biogesic pill dispenser
#define cremils 12 // servo for cremils pill dispenser
#define citirizene 11 // servo for citirizene pill dispenser
#define mefenamic 10 // servo for mefinamic pill dispenser

#define lockservo 9 // locking system for pills lock

#define wheel1 8 // wheel activator
#define wheel2 7 // wheel activator
#define wheel3 6 // wheel activator
#define wheel4 5 // wheel activator

#define echo 4 // sensor for distance
#define trig 3 // sensor for distance


#include <Servo.h>

Servo lock;  // create Servo object to control a servo
Servo biogesic_servo;
Servo cremils_servo; 
Servo citirizene_servo; 
Servo mefenamic_servo;



void setup() {
  // put your setup code here, to run once:
  lock.attach(lockservo); 
  biogesic_servo.attach(biogesic); 
  cremils_servo.attach(cremils); 
  citirizene_servo.attach(citirizene); 
  mefenamic_servo.attach(mefenamic); 

}

void loop() {
  // put your main code here, to run repeatedly:

}





void dropBiogesic(){  
}

void restartBiogesic(){  
}

void dropCremils(){  
}
void restartCremils(){  
}


void dropCitirizene(){  
}
void restartCitirizene(){  
}

void dropMefenamic(){  
}
void restartMefenamic(){  
}


void lockingSystem( bool open_back ){
  uint8_t pos = 0;    // variable to store the servo position

  if (open_back){
    // If the user want to open the back of the machine
        
    for (pos = 0; pos <= 90; pos += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      lock.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15 ms for the servo to reach the position
    }

  } else{
    
    // If the user want to lock the back of the machine
    for (pos = 90; pos >= 0; pos += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      lock.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15 ms for the servo to reach the position
    }
  }
}


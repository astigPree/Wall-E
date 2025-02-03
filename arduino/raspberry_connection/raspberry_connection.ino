



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() { 

  // Check if there is any incoming data from the serial port
  if (Serial.available() > 0) {
    // Read the incoming data from the serial port and store it in the 'data' variable
    // The '\n' character is used to mark the end of the incoming data. The readStringUntil() function reads all characters until it encounters a newline character.
    // The readStringUntil() function returns the entire string received, excluding the newline character.
    String data = Serial.readStringUntil('\n'); // Read the incoming data until a newline character
 

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

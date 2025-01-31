
int led = 3;
int but = 2;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW); // Ensure the LED is off at the start
  pinMode(but, INPUT); // Set the button as an input with a pull-up resistor
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // Read the incoming data until a newline character
    if (data == "ON") {
      digitalWrite(led, HIGH); // Turn the LED on
    } else if (data == "OFF") {
      digitalWrite(led, LOW); // Turn the LED off
    }
  }
  
  if (digitalRead(but) == HIGH) {
    Serial.println("Button pressed");
  }
}

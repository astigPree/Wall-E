


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


void setup() {
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

  Serial.begin(115600); 
}

void loop() {
  // Read blue and red frequencies from sensor 1
  int blue1 = readColor(S2, S3, LOW, HIGH, sensorOut); // Blue filter
  int red1 = readColor(S2, S3, LOW, LOW, sensorOut);   // Red filter

  // Read blue and red frequencies from sensor 2
  int blue2 = readColor(S22, S32, LOW, HIGH, sensorOut2); // Blue filter
  int red2 = readColor(S22, S32, LOW, LOW, sensorOut2);   // Red filter

  Serial.print("LEFT BLUE : ");
  Serial.println(blue1);
  Serial.print("LEFT RED : ");
  Serial.println(red1);


  // Serial.print("RIGHT BLUE : ");
  // Serial.println(blue2);
  // Serial.print("RIGHT RED : ");
  // Serial.println(red2);
  delay(500);
}


int readColor(int S2Pin, int S3Pin, int s2State, int s3State, int sensorPin) {
  digitalWrite(S2Pin, s2State);
  digitalWrite(S3Pin, s3State);
  // return pulseIn(sensorPin, LOW); // Measure the frequency for the selected color
  return pulseIn(sensorPin, LOW, 100000); // 100ms timeout

}

int trigPin = 9;
int echoPin = 10;
int proxPin = 8;
int ledPin = 6;
int buzzer = 5;
int tempPin = A0;

int drowsy = 0;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(proxPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzer, OUTPUT);

  digitalWrite(buzzer, HIGH);
  digitalWrite(ledPin, HIGH);

  Serial.begin(9600);
}

void loop() {

  long duration;
  int distance;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  // -------- PROXIMITY --------
  int proxState = digitalRead(proxPin);

  // -------- TEMPERATURE --------
  int tempValue = analogRead(tempPin);
  float temperature = tempValue * (5.0 / 1023.0) * 100;

  // -------- READ FROM PYTHON (FIXED) --------
  while (Serial.available() > 0) {
    char data = Serial.read();

    if (data == '1') {
      drowsy = 1;
    } 
    else if (data == '0') {
      drowsy = 0;
    }
  }

  // -------- FINAL CONTROL (ONLY PYTHON, ACTIVE LOW) --------
  if (drowsy == 1) {
    digitalWrite(buzzer, LOW);   // ON
    digitalWrite(ledPin, LOW);   // ON
  } else {
    digitalWrite(buzzer, HIGH);  // OFF
    digitalWrite(ledPin, HIGH);  // OFF
  }

  // -------- DEBUG PRINT --------
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.print(" | Proximity: ");
  Serial.print(proxState);
  Serial.print(" | Temp: ");
  Serial.println(temperature);

  delay(200);
}
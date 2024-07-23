int motorLeftPin1 = 12;
int motorLeftPin2 = 14;
int enableLeftPin = 13;
int motorRightPin1 = 2;
int motorRightPin2 = 4;
int enableRightPin = 0;
 
const int trigPin = 16;
const int echoPin = 5;
 
#define SOUND_SPEED 0.034
 
const float thresholdDistance = 20.0;
 
long duration;
float distanceCm;
 
void setup() {
  pinMode(motorLeftPin1, OUTPUT);
  pinMode(motorLeftPin2, OUTPUT);
  pinMode(enableLeftPin, OUTPUT);
  pinMode(motorRightPin1, OUTPUT);
  pinMode(motorRightPin2, OUTPUT);
  pinMode(enableRightPin, OUTPUT);
 
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
 
  Serial.begin(115200); 
}
 
void loop() {
  distanceCm = getDistance();
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
 
  if (distanceCm < thresholdDistance) {
    stopMotors();
    delay(1000);
    rotateLeft();
    delay(1000);   //rotates left
    stopMotors();
    delay(1000);
    distanceCm = getDistance();
    if (distanceCm >= thresholdDistance) {
      moveForward();
    } else {
      rotateRight();
      delay(2000);   //rotates -180 degree i.e. right
      stopMotors();
      delay(1000);
      distanceCm = getDistance();
      if (distanceCm >= thresholdDistance) {
        moveForward();
      } else {
		rotateRight();
        delay(1000);    //turns back and goes
        stopMotors();
        delay(1000);
		moveForward();
      }
    }
  } else {
    moveForward();
  }
 
  delay(100);
}
 
void moveForward() {
  digitalWrite(enableLeftPin, HIGH);
  digitalWrite(enableRightPin, HIGH);
  digitalWrite(motorLeftPin1, LOW);
  digitalWrite(motorLeftPin2, HIGH);
  digitalWrite(motorRightPin1, HIGH);
  digitalWrite(motorRightPin2, LOW);
  Serial.println("Moving Forward");
}
 
void stopMotors() {
  digitalWrite(enableLeftPin, LOW);
  digitalWrite(enableRightPin, LOW);
  digitalWrite(motorLeftPin1, LOW);
  digitalWrite(motorLeftPin2, LOW);
  digitalWrite(motorRightPin1, LOW);
  digitalWrite(motorRightPin2, LOW);
  Serial.println("Motors Stopped");
}
 
void rotateLeft() {
  digitalWrite(enableLeftPin, HIGH);
  digitalWrite(enableRightPin, HIGH);
  digitalWrite(motorLeftPin1, HIGH);
  digitalWrite(motorLeftPin2, LOW);
  digitalWrite(motorRightPin1, HIGH);
  digitalWrite(motorRightPin2, LOW);
  Serial.println("Rotating Left");
}
 
void rotateRight() {
  digitalWrite(enableLeftPin, HIGH);
  digitalWrite(enableRightPin, HIGH);
  digitalWrite(motorLeftPin1, LOW);
  digitalWrite(motorLeftPin2, HIGH);
  digitalWrite(motorRightPin1, LOW);
  digitalWrite(motorRightPin2, HIGH);
  Serial.println("Rotating Right");
}
 
float getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  duration = pulseIn(echoPin, HIGH);
 
  return duration * SOUND_SPEED / 2;
}

//Includes
#include <Servo.h>

const int Sensor1 = A0;
      
void setup() {
  
  // initialize serial communication at 9600 bits per second:
  Serial.begin(2400);
  
  //initialize inputs
  pinMode(Sensor1, INPUT);

}

void loop() {
  int raw = analogRead(Sensor1); 
  Serial.println(raw);
  delay(500);
}

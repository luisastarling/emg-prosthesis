//Includes
#include <Servo.h>

//Constants
const int Servo1 = 6;
const int Servo2 = 9;
const int Servo3 = 10;
const int Servo4 = 11;
const int Servo5 = 13;

const int Sensor = A0;
const int thr = 600;

//Objects
Servo minimo;
Servo anelar;
Servo medio;
Servo indicador;
Servo polegar;

void setup() {
  
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  
  //initialize outputs
  pinMode(Servo1, OUTPUT);
  pinMode(Servo2, OUTPUT);
  pinMode(Servo3, OUTPUT);
  pinMode(Servo4, OUTPUT);
  pinMode(Servo5, OUTPUT);

  //initialize inputs
  pinMode(Sensor, INPUT);

  //Attach finger objects to servos
  minimo.attach(Servo1);
  anelar.attach(Servo2);
  medio.attach(Servo3);
  indicador.attach(Servo4);
  polegar.attach(Servo5);

}

void loop() {
  
  //Read sensor input
  int emg = analogRead(Sensor);
  bool activeMuscle = active(emg, thr);
  
  //Close hand
  if (activeMuscle){
    polegar.write(0);
    indicador.write(0);
    medio.write(0);
    anelar.write(0);
    minimo.write(0); 
  }
  //Delay
  delay(5000);

  //Open hand 
  polegar.write(90);
  indicador.write(90);
  medio.write(90);
  anelar.write(90);
  minimo.write(90); 
}

bool active(int sensor, int threshold){
  if (sensor < threshold) {
    return false;
  } else return true;
}

//Includes
#include <Servo.h>

//Constantes
const int Servo1 = 6;
const int Servo2 = 9;
const int Servo3 = 10;
const int Servo4 = 11;
const int Servo5 = 13;

const int Sensor1 = A0;
const int Sensor2 = A1;
const int Sensor3 = A2;

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
  pinMode(Sensor1, INPUT);
  pinMode(Sensor2, INPUT);
  pinMode(Sensor3, INPUT);

  //Attach finger objects to servos
  minimo.attach(Servo1);
  anelar.attach(Servo2);
  medio.attach(Servo3);
  indicador.attach(Servo4);
  polegar.attach(Servo5);
}

void loop() {
  //Read sensor input
  int valueSensor1 = analogRead(Sensor1);
  int valueSensor2 = analogRead(Sensor2);
  int valueSensor3 = analogRead(Sensor3);

  //Sensor activation
  bool activeSensor1 = active(valueSensor1, thr);
  bool activeSensor2 = active(valueSensor2, thr);
  bool activeSensor3 = active(valueSensor3, thr);

  //Servo activation
  if (activeSensor1){
    polegar.write(0);
  }else polegar.write(90);

  if (activeSensor2){
    medio.write(0);
    indicador.write(0);
  }else{
    medio.write(90);
    indicador.write(90);
  }

  if (activeSensor3){
    minimo.write(0);
    anelar.write(0);
  }else{
    minimo.write(90);
    anelar.write(90);
  }

  //Delay
  delay(500);
}

bool active(int sensor, int thresh){
  if (sensor < thresh) {
    return false;
  } else return true;
}

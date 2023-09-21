//-------------------------------------------------------
//-------------------------------------------------------
//Librerias
#include <ModbusIP_ESP8266.h>
#include <PID_v1.h>
#include <Servo.h>
#include <WiFi.h>
#include <LiquidCrystal_I2C.h>
#include <MedianFilterLib.h>
//-------------------------------------------------------
//-------------------------------------------------------
//GPIO Pins

//Ultrasonicos
  //Elevado
  int analogValue;
  MedianFilter<int> medianFilter(5);
  int median;
  float Level;
  //#define Trig1 25
  //#define Echo1 33
  float Elevado;
  
  //Cisterna 
  #define Trig2 33
  #define Echo2 32
  float Cisterna;

//Relee
#define Relee 12

//Conductividad
#define Conduc 34
//-------------------------------------------------------
//-------------------------------------------------------
//Servo
Servo myServo;
#define servoPin 13
uint16_t Pos = 60;
//-------------------------------------------------------
//-------------------------------------------------------
//Modbus Registers Offsets
#define Relee_Coil 0
#define Conduc_Coil 1
#define Mode_Coil 2
#define Servo_Register 3
#define Elevado_Register 4
#define Cisterna_Register 6
#define Setpoint_Register 8
#define Output_Register 12

ModbusIP mb;
//-------------------------------------------------------
//-------------------------------------------------------
LiquidCrystal_I2C lcd(0x27,20,4); 
//-------------------------------------------------------
//-------------------------------------------------------
//PID
double Setpoint, Input, Output;
double Kp=12.31, Ki=0.0002652, Kd=131.2;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
//-------------------------------------------------------
//-------------------------------------------------------
//Timer
hw_timer_t * timer = NULL;
volatile bool state = false;

void IRAM_ATTR onTimer(){
  state = true;
  }
//-------------------------------------------------------
//------------------------------------------------------- 
//Tipo de estructura para convertir de Float a 2 uint16 
union FloatToUint16{
  float FloatValue;
  uint16_t uint16Value[2];
  };
//-------------------------------------------------------
//-------------------------------------------------------
//Funcion para calcular la distacion de los ultrasonicos
float Distance(int EchoPin, int trigPin){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  float duration_us = pulseIn(EchoPin,HIGH);
  return 0.017 * duration_us;
  }
//-------------------------------------------------------

void setup() {
  //-------------------------------------------------------
  //Puerto Serie
  Serial.begin(115200); 
  //-------------------------------------------------------
  //-------------------------------------------------------
  //Wifi
  WiFi.begin("iPhone 6 Plus","melon123445");
 
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
    }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  //-------------------------------------------------------
  //-------------------------------------------------------
  //Modbus Communication
  mb.server();
  
  mb.addCoil(Relee_Coil);
  mb.addCoil(Conduc_Coil);
  mb.addCoil(Mode_Coil);
  
  mb.addHreg(Servo_Register);
  
  mb.addHreg(Elevado_Register);
  mb.addHreg(Elevado_Register+1);
  
  mb.addHreg(Cisterna_Register);
  mb.addHreg(Cisterna_Register+1);
  
  mb.addHreg(Setpoint_Register);
  mb.addHreg(Setpoint_Register+1);
  
  mb.addHreg(Output_Register);
  mb.addHreg(Output_Register+1);
  //-------------------------------------------------------
  //-------------------------------------------------------
  //GPIO Declarations
  //pinMode(Trig1,OUTPUT);
  //pinMode(Echo1,INPUT);
  pinMode(Trig2,OUTPUT);
  pinMode(Echo2,INPUT);
  pinMode(Conduc,INPUT);  
  pinMode(Relee,OUTPUT);
  
  digitalWrite(Relee,LOW);
  //-------------------------------------------------------
  //-------------------------------------------------------
  //Configuracion Timer 1s
  timer = timerBegin(0,80,true);
  timerAttachInterrupt(timer, &onTimer, true);
  timerAlarmWrite(timer,1000000, true);
  timerAlarmEnable(timer);
  //-------------------------------------------------------
  //-------------------------------------------------------
  //LCD Configuration
  lcd.init(); 
  lcd.backlight();
  lcd.setCursor(0,1);
  lcd.print("Distance:");
  lcd.setCursor(0,2);
  lcd.print("Distance:");
  lcd.setCursor(0,3);
  lcd.print("Pos:");
  lcd.setCursor(10,3);
  lcd.print("Con:");
  //-------------------------------------------------------
  //-------------------------------------------------------
  //Servo Configuration
  myServo.attach(servoPin);
  myServo.write(Pos);//(60-140)
  //-------------------------------------------------------
  //-------------------------------------------------------
  //PID Configuration
  myPID.SetTunings(Kp, Ki, Kd);
  myPID.SetMode(AUTOMATIC);
  myPID.SetOutputLimits(60, 140);
  myPID.SetSampleTime(1000);
  //-------------------------------------------------------
  //-------------------------------------------------------
  analogReadResolution(12);
  pinMode(35,INPUT);
}

void loop() {
  /*
  #include <MedianFilterLib.h>

String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete
int analogValue;
MedianFilter<int> medianFilter(15);
int median;
float Level;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(35,INPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
    if (stringComplete) {
      if(inputString == "-\n"){
        for(int i =0; i<4000;i++){
            analogValue = analogReadMilliVolts(35);
            median = medianFilter.AddValue(analogValue);
            Level = 0.03176 * median - 70.35;
            Serial.println(Level);
            delay(250);
          }  
        }
       else{
          Serial.println();
          Serial.print(inputString);
          Serial.println();
       }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }

}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}*/
  if(Elevado >= 13.5){
      digitalWrite(Relee,LOW);
      }
  if(Cisterna >= 100){
      myServo.write(0);
      }
      
  mb.task();
  //Si el modo manual esta activo Actualizar la posicion del Servo
  if(!mb.Coil(Mode_Coil)){
      Pos = map(mb.Hreg(Servo_Register),0,100,60,140);
      myServo.write(Pos);
      digitalWrite(Relee,mb.Coil(Relee_Coil)); //Actualizar el estado del mootor
    }
  
  
  //Este if se ejecuta cada 1seg
  if(state){
    //Update Conduct
    mb.Coil(Conduc_Coil,digitalRead(Conduc)); //Actualizar el valor del sensor de Conductividad
    //Actualizar el valor de Setpoint para el PID si el modo automatico esta activo
    FloatToUint16 SetpointFloat;
    SetpointFloat.uint16Value[1] = mb.Hreg(Setpoint_Register);
    SetpointFloat.uint16Value[0] = mb.Hreg(Setpoint_Register+1);
    Setpoint = SetpointFloat.FloatValue;
    Serial.print("Setpoint:");
    Serial.println(Setpoint);
  
  //Calcular y actualizar el nivel del tanque elevado
    FloatToUint16 dato;

    analogValue = analogReadMilliVolts(35);
    median = medianFilter.AddValue(analogValue);
    //Level = 

    dato.FloatValue = 0.03176 * median - 70.35;
    Elevado=dato.FloatValue;
    Serial.print("Elevado:");
    Serial.println(Elevado);
    mb.Hreg(Elevado_Register,dato.uint16Value[1]);
    mb.Hreg(Elevado_Register+1,dato.uint16Value[0]);

    //Calcular y actualizar el nivel del tanque cisterna
    FloatToUint16 dato1;
    dato1.FloatValue = 20.2 - Distance(Echo2,Trig2);
    Cisterna=dato1.FloatValue;
    Serial.print("Cisterna:");
    Serial.println(Cisterna);
    mb.Hreg(Cisterna_Register,dato1.uint16Value[1]);
    mb.Hreg(Cisterna_Register+1,dato1.uint16Value[0]);
    
    //Si el modo automatico esta activo ejecutar el PID
    if(mb.Coil(Mode_Coil)){
      Input = dato.FloatValue;
      myPID.Compute();
      Pos = Output;
      myServo.write(Pos);
      mb.Hreg(Servo_Register,Pos);
      //Actualizar Registro de Output del PID
      FloatToUint16 datoOutput;
      datoOutput.FloatValue = (float)Output;
      mb.Hreg(Output_Register,datoOutput.uint16Value[1]);
      mb.Hreg(Output_Register+1,datoOutput.uint16Value[0]);
      }
    //Cargar valores en la LCD    
    lcd.setCursor(9,1);
    lcd.print(dato.FloatValue);
    lcd.setCursor(9,2);
    lcd.print(dato1.FloatValue);
    lcd.setCursor(5,3);
    lcd.print(mb.Hreg(Servo_Register));
    lcd.setCursor(15,3);
    lcd.print(mb.Coil(Conduc_Coil));
    state = false;
  }
}
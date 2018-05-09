//Encender y apagar dos LED
//Se crean las variables de los pines de los leds y una variable que conecta con Python
const int LED1=13;
const int LED2=12;
int movimiento = 0;
void setup()
{
  //Se inicializa los pines y el serial
  pinMode(LED1,OUTPUT);
  pinMode(LED2,OUTPUT);
  Serial.begin(9600);
}
void loop()
{
  //Se enciende el led 1
  digitalWrite(LED1,HIGH);
  //Se verifica que el Serial reciba algo
  if(Serial.available() > 0){
    //Se lee la variable que conecta con Python
    movimiento = Serial.read(); 
    //Si es igual a uno los dos leds se encienden 
    if(movimiento == '1'){
      digitalWrite(LED1,HIGH);
      digitalWrite(LED2,HIGH);
    }
    //Sino se apaga el led 2
    else{
      digitalWrite(LED1,HIGH);
      digitalWrite(LED2,LOW);
    }
  }
  
}

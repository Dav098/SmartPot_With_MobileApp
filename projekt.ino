//    FOTOREZYSTOR
#define FOTOREZYSTOR A1

//    DHT11
#include "DHT.h"          // biblioteka sensorów DHTxx  
#define DHTPIN 2          // wyjście danych sensora jest dołączone
#define DHTTYPE DHT11     // DHT11
DHT dht(DHTPIN, DHTTYPE);

//    LED_STRIP
#define redPin 11
#define greenPin 10
#define bluePin 9

//    CZUJNIK WILGOTNOŚCI GLEBY (CWG)
#define sensor_A0 A0       // podłączenie od A0 na czujniku do A0 na Arduino
#define sensor_D0 4        // podłączenie od D0 na czujniku do pinu 4 na Arduino
int wartosc_A0;            // zmienna dla wartości A0
int wartosc_D0;            // zmienna dla wartości D0

//------------------------SETUPY-----------------------------------------------------

void setup_dht11()
  {
    dht.begin();            // inicjalizacja czujnika
  }

void setup_led(){
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void setup_CWG() {
  pinMode(4, INPUT);    // ustawienie pinu 4 jako wejście
 
}
    

//-------------------------FUNKCJE--------------------------------------------------- 
float t;
float h;
void dht11()
{
  t = dht.readTemperature();  // odczyt temperatury
  h = dht.readHumidity();     // odczyt wilgotności powietrz
  // czy odczytano wartości?
  if (isnan(t) || isnan(h))
  {
    Serial.println("Blad odczytu danych z czujnika!");
  }
  else
  {
    //wysyłamy wyniki przez port szeregowy
    Serial.print('t');
    Serial.print(t); //temperatura powietrza w *C
    delay(200);
    Serial.print('h');
    Serial.print(h); //wilgotnosc powietrza w %
    delay(200);
  }
     
}



void TurnOn_Led()
{
  analogWrite(redPin, 255);
  analogWrite(greenPin, 255);
  analogWrite(bluePin, 255);
  Serial.print("LLed On");
  delay(200);
}
void TurnOff_Led()
{
  analogWrite(redPin, 0);
  analogWrite(greenPin, 0);
  analogWrite(bluePin, 0);
  Serial.print("LLed Off");
  delay(200);
}



void CWG()
{
 wartosc_A0 = analogRead(sensor_A0);      // pobranie wartości z A0
 wartosc_D0 = digitalRead(sensor_D0);     // pobranie wartości z D0

 Serial.print('d');
 Serial.print(wartosc_D0);    //Wartość z D0
 delay(200);
 Serial.print('a');
 Serial.print(wartosc_A0);    //Wartość z A0
 delay(200);                              // opóźnienie pomiędzy kolejnymi odczytami
 } 
 
//////////////////////////////////////////////////////////////////////////////////////////
void setup()
  {
    Serial.begin(9600);   // uruchomienie monitora szeregowego
    setup_dht11();
    setup_led();
    setup_CWG();
  }
  
void loop()
{
  dht11();
  CWG();
  if(analogRead(FOTOREZYSTOR) <= 200)   //jeśli wartość światła jest mniejsza od ... to wykonaj...
  { 
    TurnOn_Led();
  }
  else{
    //jeśli jest jasno to...
    TurnOff_Led();
  }
  
  delay(30000);
  //delay(3600000);   //godzinne opoznienie
  
}
  
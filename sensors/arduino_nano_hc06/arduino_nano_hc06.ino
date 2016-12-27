/*
  Desc:   Permet d'envoyer via une connexion BT, la tempértature et le taux d'humidité d'une sonde DHT22
  Auteur: MathPis

  Matériel:
  Sonde: DHT22
  Module BT HC-06
  Arduino Nano

  Library from : https://github.com/djsb/arduino-websocketclient
*/

#include <SoftwareSerial.h>
//#include "WSClient.h"
#include "DHT.h"
#include <ArduinoJson.h>

#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
#define DHTPIN 3
DHT dht(DHTPIN, DHTTYPE);

#define ControlPIN 13

#define BTtxPIN 10  
#define BTrxPIN 11  
SoftwareSerial BT(BTtxPIN, BTrxPIN);  // connect TX->D10, RX->D11, Vcc->3.3V, GND->GND 

#define captureDelay 10000  // 2 minutes

void setup() {
  
  // set digital pin to control as an output
  pinMode(ControlPIN, OUTPUT);

  // Bluetooth
  // --------------------------
  // set the data rate for the SoftwareSerial port
  BT.begin(9600);
  // Send test message to other device
  BT.println("Hello from Arduino");

  // Port Série
  // --------------------------
  Serial.begin(115200);
  Serial.print("Test du DHT-");
  Serial.println(DHTTYPE);

  // Capteur
  // --------------------------
  dht.begin();

}

char a; // stores incoming character from other device

void loop() {


  if (BT.available())
  // if text arrived in from BT serial...
  {
    a=(BT.read());
    if (a=='1')
    {
      digitalWrite(ControlPIN, HIGH);
      Serial.println("LED on");
    }
    if (a=='2')
    {
      digitalWrite(ControlPIN, LOW);
      Serial.println("LED off");
    }
    if (a=='?')
    {
      Serial.println("Send '1' to turn LED on");
      Serial.println("Send '2' to turn LED off");
    }   
    // you can add more "if" statements with other characters to add more commands
  }

  
  // Wait a few seconds between measurements.
  delay(captureDelay);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  //float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // --- Envoi temperature  --------------------------------
  char BuffTemp[100];
  StaticJsonBuffer<200> jsonBufferTemp;
  JsonObject& jsonTemperature = jsonBufferTemp.createObject();
  
  jsonTemperature["typeReq"] = "SET";
  
  jsonTemperature["msg"] = "setTemperature";
  
  JsonArray& param = jsonTemperature.createNestedArray("params");
  JsonObject& jsonTempVal = jsonBufferTemp.createObject();
  jsonTempVal["temperature"] = t;
  param.add(jsonTempVal); // 2 est le nombre de decimal à afficher
  
  jsonTemperature.printTo(BuffTemp, sizeof(BuffTemp));
  BT.println(BuffTemp);
  Serial.println(BuffTemp);
  // -------------------------------------------------------

  // --- Envoi temperature  --------------------------------
  char BuffHHumidite[70];
  StaticJsonBuffer<200> jsonBufferHumid;
  JsonObject& jsonHumidite = jsonBufferHumid.createObject();
  
  jsonHumidite["typeReq"] = "SET";
  
  jsonHumidite["msg"] = "setHumidite";
  
  JsonArray& paramH = jsonHumidite.createNestedArray("params");
  JsonObject& jsonHumidVal = jsonBufferHumid.createObject();
  jsonHumidVal["humidite"] = h;
  paramH.add(jsonHumidVal); 
  
  jsonHumidite.printTo(BuffHHumidite, sizeof(BuffHHumidite));
  BT.println(BuffHHumidite);
  Serial.println(BuffHHumidite);
  // -------------------------------------------------------

  // Envoi des donnees sur la lisaison serie pour DEBUG
  //String message = String(h,2) + "//" + String(t,2);
  //Serial.println(BuffTemp);
}


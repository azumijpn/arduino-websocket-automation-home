/*
  Desc: Affiche le différentiel de température entre deux sondes et pilote la chaudière.
  Auteur: zasquash

  Matériel:
  Sonde: 2 x DS18B20
  Arduino Ethernet PoE
  Relay 5v

  Library from : https://github.com/djsb/arduino-websocketclient
*/

#include <SPI.h>
#include <Ethernet.h>
#include "WSClient.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>

// Define a maximum framelength to 64 bytes. Default is 256. Don't Work !!!
#define MAX_FRAME_LENGTH 256

//PIN capteurs
#define SENSORA 2

//Définition des capteurs
OneWire TMP_CUMULUS(SENSORA);

DallasTemperature sensor_cumulus(&TMP_CUMULUS);

/*################# Parameters #################*/

const String LOCATION = "CUMULUS";          // Emplacement du capteur arduino
const String HOSTNAME = "ARDUINO_ETHERNET"; // Name arduino
#define IPSERVER   "192.168.100.245"        // Serveur distant
#define PORT        8000                    // Port du serveur distant
#define PATH        "/"                     // Path
#define TIMECYCLE   10                    // Time in ms
#define BAUDRATE    115200                  //Serial speed

// Ethernet Configuration
byte mac[] = {0x52, 0x4F, 0x43, 0x4B, 0x45, 0x54};
IPAddress ip(192, 168, 100 , 150);
IPAddress subnet(255, 255, 255, 0);
//IPAddress myDNS(192, 168, 100, 245);
//IPAddress gateway(192, 168, 100, 254);

/*################# End Parameters #################*/

EthernetClient client;

// Websocket initialization
WSClient websocket;

void transmission(char *objJson) {

  if (client.connect(IPSERVER, PORT)) {
    Serial.println("Connected");

    if (websocket.handshake(client)) {
      Serial.println("Handshake successful");

      String data = websocket.getData();
  
      if (data.length() > 0) {
         Serial.print("Received data: ");
         Serial.println(data);
      }

      websocket.sendData(objJson);

    } else {
      Serial.println("Handshake failed.");
    }
 
  } else {
    Serial.println("Connection failed.");
  }

  delay(500);
  websocket.disconnect();
}

void setup() {

  Serial.begin(BAUDRATE);

  //Init Ethernet
  Ethernet.begin(mac, ip, subnet);
  //Ethernet.begin(mac, ip, subnet, myDNS, gateway);
  Serial.print("IP Arduino : ");
  Serial.println(Ethernet.localIP());

  delay(1000);

  sensor_cumulus.begin();

  delay(100);

  // Define path and host for Handshaking with the server
  websocket.path = PATH;
  websocket.host = IPSERVER;

}

void loop() {

  char Buff[70];
  StaticJsonBuffer<200> jsonBufferTemp;
  
  sensor_cumulus.requestTemperatures();

  float temperature = (sensor_cumulus.getTempCByIndex(0));

  JsonObject& jsonTemperature = jsonBufferTemp.createObject();
  jsonTemperature["msg"] = "setTemperature";
  jsonTemperature["location"] = LOCATION;
  jsonTemperature["temperature"] = temperature;

  jsonTemperature.printTo(Buff, sizeof(Buff));

  transmission(Buff);
  
  delay(TIMECYCLE);
}

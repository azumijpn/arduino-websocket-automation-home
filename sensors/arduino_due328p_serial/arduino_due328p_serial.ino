/*
  Desc: Affiche le différentiel de température entre deux sondes et pilote la chaudière.
  Auteur: zasquash

  Matériel:
  Sonde: 1 x DS18B20
  Arduino Duemilanove 328p
*/

#include <SPI.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>
#include <avr/wdt.h>

//PIN capteurs
#define SENSORA 2

//Définition des capteurs
OneWire TMP_CUMULUS(SENSORA);

DallasTemperature sensor_cumulus(&TMP_CUMULUS);

/*################# Parameters #################*/

const String SENSOR = "ARDUINO_DUE_SERIAL"; // Name arduino
#define TIMECYCLE   2000                    // Time in ms
#define BAUDRATE    115200                  //Serial speed

/*################# End Parameters #################*/

//watchdog
//void reset_software(void) {
//  wdt_enable(WDTO_15MS);
//  for (;;);
//}

void transmission(char *objJson) {
  if (Serial.available()) {
    //Serial.write(objJson);
  } else {
//    reset_software();
  }
}

void receive() {
  char data = Serial.read();
  char str[2];
  str[0] = data;
  str[1] = '\0';
  Serial.print("Received data: ");
  Serial.print(str);

}

void setup() {

  Serial.begin(BAUDRATE);
  delay(1000);

  sensor_cumulus.begin();

  delay(100);
}

void loop() {

  char Buff[100];
  StaticJsonBuffer<200> jsonBufferTemp;

  sensor_cumulus.requestTemperatures();

  float temperature = (sensor_cumulus.getTempCByIndex(0));

  JsonObject& jsonTemperature = jsonBufferTemp.createObject();
  jsonTemperature["msg"] = "setTemperature";
  jsonTemperature["sensor"] = SENSOR;
  jsonTemperature["temperature"] = temperature;

  jsonTemperature.printTo(Buff, sizeof(Buff));
  Serial.println(Buff);
  delay(5000w);
  
  Serial.write(Buff);

  //receive();
  //transmission(Buff);

  delay(TIMECYCLE);
}

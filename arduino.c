#include <DHT11.h>
#include <ArduinoJson.h>

#define DHT11PIN 8

DHT11 dht11(8);

const int trigPin = 9;
const int echoPin = 10;
const int waterPumpPin = 7;
const int waterPlantPin = 6;
const int UVPin = 5;
const int acPin = 4;
const int heaterPin = 3;
float duration, distance;


void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(waterPumpPin, OUTPUT);
  pinMode(waterPlantPin, OUTPUT);
  pinMode(UVPin, OUTPUT);
  pinMode(acPin, OUTPUT);
  pinMode(heaterPin, OUTPUT);

  pinMode(echoPin, INPUT);
}

void loop() {
  int currentMoistureLevel = analogRead(A0);

  int temperature = 0;
  int humidity = 0;

  // Attempt to read the temperature and humidity values from the DHT11 sensor.
  int result = dht11.readTemperatureHumidity(temperature, humidity);

  // Check the results of the readings.
  // If the reading is successful, print the temperature and humidity values.
  // If there are errors, print the appropriate error messages.

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration * .0343) / 2;

  //distance = map(distance, 0, 300, 0, 100);
  //currentMoistureLevel =  map(currentMoistureLevel, 0, 1023, 100, 0);

  //delay(2000);


  if (result == 0) {
    Serial.print(currentMoistureLevel);
    Serial.print(";");
    Serial.print(temperature);
    Serial.print(";");
    Serial.println(distance);
  }  //delay(200);


  if (Serial.available() > 0) {
    // Read the incoming data
    String jsonString = Serial.readStringUntil('\n');

    // Parse JSON
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, jsonString);

    // Check for parsing errors
    if (error) {
      //Serial.print(F("Error parsing JSON: "));
      //Serial.println(error.c_str());
      return;
    }


    // Get the value of the 'success' key as a string
    String waterPumpValue = doc["water_pump"];
    String waterPlantValue = doc["water_plant"];
    String lampValue = doc["lamp"];
    String acValue = doc["ac"];
    String heaterValue = doc["heater"];

    if (waterPumpValue == "true") {
      
      digitalWrite(waterPumpPin, HIGH);
    }
    if (waterPumpValue == "false") {
      digitalWrite(waterPumpPin, LOW);
    }
    if (waterPlantValue == "true") {
      digitalWrite(waterPlantPin, HIGH);
    }
    if (waterPlantValue == "false") {
      digitalWrite(waterPlantPin, LOW);
    }
    if (lampValue == "true") {
      digitalWrite(UVPin, HIGH);
    }
    if (lampValue == "false") {
      digitalWrite(UVPin, LOW);
    }
    if (acValue == "true") {
      digitalWrite(acPin, HIGH);
    }
    if (acValue == "false") {
      digitalWrite(acPin, LOW);
    }
    if (heaterValue == "true") {
      digitalWrite(heaterPin, HIGH);
    }
    if (heaterValue == "false") {
      digitalWrite(heaterPin, LOW);
    }
    //digitalWrite(waterPlantPin, HIGH);
  }
}
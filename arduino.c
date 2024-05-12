#include <DHT11.h>
#define DHT11PIN 4

DHT11 dht11(4); // Create an instance of the DHT11 class with pin 4 as the parameter.

const int trigPin = 9;  
const int echoPin = 10; 

float duration, distance;  


void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate.
  pinMode(A0, INPUT); // Set pin A0 as INPUT for reading moisture level.
  pinMode(trigPin, OUTPUT); // Set trigPin as OUTPUT for ultrasonic sensor.
  pinMode(echoPin, INPUT);  // Set echoPin as INPUT for ultrasonic sensor.

}

void   loop() {
  int currentMoistureLevel = analogRead(A0); // Read the moisture level from pin A0.
  
  int temperature = 0;
  int humidity = 0;

  // Attempt to read the temperature and humidity values from the DHT11 sensor.
  int result = dht11.readTemperatureHumidity(temperature, humidity);

  // Check the results of the readings.
  // If the reading is successful, print the temperature and humidity values.
  // If there are errors, print the appropriate error messages.

  digitalWrite(trigPin, LOW); // Set trigPin to LOW state.
  delayMicroseconds(2); // Wait for 2 microseconds.
  digitalWrite(trigPin, HIGH); // Set trigPin to HIGH state.
  delayMicroseconds(10); // Wait for 10 microseconds.
  digitalWrite(trigPin, LOW); // Set trigPin to LOW state.

  duration = pulseIn(echoPin, HIGH); // Read the duration of the pulse from echoPin.
  distance = (duration*.0343)/2; // Calculate distance based on the duration of the pulse.

  //distance = map(distance, 0, 300, 0, 100); // Optional mapping of distance.
  //currentMoistureLevel =  map(currentMoistureLevel, 0, 1023, 100, 0); // Optional mapping of moisture level.

  //delay(2000); // Optional delay.

  if (result == 0){
    Serial.print(currentMoistureLevel); // Print current moisture level.
    Serial.print(";");
    Serial.print(temperature); // Print temperature.
    Serial.print(";");
    Serial.println(distance); // Print distance.
  }//delay(200); // Optional delay.
}

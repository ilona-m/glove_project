#include <WiFiNINA.h>

char ssid[] = "";        // Network name
char pass[] = "";        // Network password
int status = WL_IDLE_STATUS;      // Connection status
WiFiServer server(80);            // Server socket

WiFiClient client = server.available();

const int sensorPin = A0;  // Analog input pin that the sensor is attached to
const int sensorPin2 = A1;
const int sensorPin3 = A2;
const int sensorPin4 = A3;
const int sensorPin5 = A4;
const int sensorPin6 = A5;
const int sensorPin7 = A6;


int sensorValue = 0; // Raw value read from the pin
int sensorValue2 = 0;
int sensorValue3 = 0;
int sensorValue4 = 0;
int sensorValue5 = 0;
int sensorValue6 = 0;
int sensorValue7 = 0;

String processedValue = ""; // Value calculated from the raw value
bool printToClient = false; // Used for controlling the board

void setup() {
  // Initialize serial communications at 9600 bps:
  Serial.begin(9600);

  while (!Serial) {}

  // Initialize pins
  pinMode(sensorPin, INPUT);
  pinMode(sensorPin2, INPUT);
  pinMode(sensorPin3, INPUT);
  pinMode(sensorPin4, INPUT);
  pinMode(sensorPin5, INPUT);
  pinMode(sensorPin6, INPUT);
  pinMode(sensorPin7, INPUT);


  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to network
    status = WiFi.begin(ssid, pass);

    // Wait 10 seconds for connection:
    delay(10000);
  }

  // Start server
  server.begin();

  Serial.println("Successfully connected to WiFi");
  
  // Print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

void loop() {
  client = server.available();

  // If there is a client, process the request
  if (client) {
    Serial.println("Client connected");

    // Start a new loop for handling the connection
    while (client.connected()) {
      // Check for incoming data, and read it one byte at a time
      if (client.available()) {
        byte command = client.read();
        // If command is 0, stop printing
        // If it is 1, start printing
        if (command == '0') {
          digitalWrite(LED_BUILTIN, LOW);
          printToClient = false;
        } else if (command == '1') {
          digitalWrite(LED_BUILTIN, HIGH);
          printToClient = true;
        }
      }

      // Read the analog in value:
      sensorValue = analogRead(sensorPin);
      sensorValue2 = analogRead(sensorPin2);
      sensorValue3 = analogRead(sensorPin3);
      sensorValue4 = analogRead(sensorPin4);
      sensorValue5 = analogRead(sensorPin5);
      sensorValue6 = analogRead(sensorPin6);
      sensorValue7 = analogRead(sensorPin7);


      if (printToClient) {
        //Send the results to the Client
       char text[50];
       int sensorArray[7] = {sensorValue, sensorValue2, sensorValue3, sensorValue4, sensorValue5, sensorValue6, sensorValue7};
       for (byte i = 0; i < 7; i++) {
         itoa(sensorArray[i], text, 10);
         client.print(text);
         if(i<6){
          client.print(",");
         }
       }
       client.println(); // Send a newline character to mark the end of the line
      }

      delay(2);
    }
    
    Serial.println("Client disconnected");
  }
}

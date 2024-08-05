#include <WiFi.h>
#include <ESP32Firebase.h>
#include <OneWire.h>
#include "mbedtls/rsa.h"
#include "mbedtls/entropy.h"
#include "mbedtls/ctr_drbg.h"
#include "mbedtls/pk.h"
#include <DallasTemperature.h>
#include <AESLib.h>
#include <Base64.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// Define the NTP client
WiFiUDP udp;
NTPClient timeClient(udp, "pool.ntp.org", 3600 * 3, 60000);  // NTP server, time offset in seconds, update interval

const char *publicKey = "-----BEGIN PUBLIC KEY-----\n" \
                        "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkP42SZnv0PC1M9Dw7QqQ\n" \
                        "RH22DIQnGEYN0Ul2CYKvUVsOqqev2MzJznevofoC857Gw89e2tUOVSwlucYH5A+e\n" \
                        "u5AXGoRcid6jhgIoNmGL0IaKLFHuvCOgG6gT4mvrH+q5BeeFN7bxgMV3+enQEPKj\n" \
                        "27Qgdwr1vAXDVnw0kQhOJx0IuVHWubVJs/WAzMfFNGG0DWrSJqT2R8/GwtLiZWJb\n" \
                        "j6Yfz496EDhbbMV4696OH+eol4EPM2JUDZlPWqJ+qSrrhdiAlMXCxmg0FK64R5qF\n" \
                        "cA2gDqLEClTP0x0Jm/05bn/0NTg8XwQnO/88ZARVSjiR5o92D+tKDTbHsRqp5Ibv\n" \
                        "zwIDAQAB\n" \
                        "-----END PUBLIC KEY-----\n";

#define WIFI_SSID "Big Boyz"
#define WIFI_PASSWORD "Placement"

#define ANALOG_PIN 27

const String USER_ID = "WgamA6avjxRUSs4hb4lAPQbNkij1";

// Firebase project details
#define FIREBASE_HOST "https://fish-farm-3747d-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "AIzaSyD0ngR0OSDh8kDzsB-FENHewcb-Se6cDFw"

// Initialize Firebase Data object
Firebase firebase(FIREBASE_HOST);

// Data wire is plugged into pin 2 on the ESP32
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Variables to hold sensor readings
float temperature = 0.0;
float temp1 = 0.0;
float temp2 = 0.0;
float pH = 0.0;
float my_pH = 0.0;

mbedtls_pk_context pk;
mbedtls_entropy_context entropy;
mbedtls_ctr_drbg_context ctr_drbg;

void setup() {
  Serial.begin(9600);

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to Wi-Fi...");
  }
  Serial.println("Connected to Wi-Fi");

  // Initialize NTP Client
  timeClient.begin();
  timeClient.update();

  // Initialize the DS18B20 sensor
  sensors.begin();

  randomSeed(analogRead(ANALOG_PIN));

  // Initialize library tools for RSA encryption
  mbedtls_pk_init(&pk);
  mbedtls_entropy_init(&entropy);
  mbedtls_ctr_drbg_init(&ctr_drbg);

  const char *pers = "";
  int ret = mbedtls_ctr_drbg_seed(&ctr_drbg, mbedtls_entropy_func, &entropy, (const unsigned char *)pers, strlen(pers));
  if (ret != 0) {
    Serial.printf("mbedtls_ctr_drbg_seed failed, returned %d\n", ret);
    while (1);
  }

  ret = mbedtls_pk_parse_public_key(&pk, (const unsigned char *)publicKey, strlen(publicKey) + 1);
  if (ret != 0) {
    Serial.printf("mbedtls_pk_parse_public_key failed, returned %d\n", ret);
    while (1);
  }
}

String getCurrentTimestamp() {
  timeClient.update();
  unsigned long epochTime = timeClient.getEpochTime();
  time_t rawTime = epochTime;
  struct tm *timeinfo = localtime(&rawTime);

  char timestamp[20];
  snprintf(timestamp, sizeof(timestamp), "%04d-%02d-%02d %02d:%02d:%02d",
           timeinfo->tm_year + 1900, timeinfo->tm_mon + 1, timeinfo->tm_mday,
           timeinfo->tm_hour, timeinfo->tm_min, timeinfo->tm_sec);
  return String(timestamp);
}

String encrypt(String plainText) {
  int ret;
  size_t olen;
  unsigned char encrypted[512];

  ret = mbedtls_pk_encrypt(&pk, (const unsigned char *)plainText.c_str(), plainText.length(),
                           encrypted, &olen, sizeof(encrypted), mbedtls_ctr_drbg_random, &ctr_drbg);
  if (ret != 0) {
    Serial.printf("mbedtls_pk_encrypt failed, returned %d\n", ret);
    return "";
  }

  // Encode encrypted data in base64
  char encoded[1024];
  int encodedLen = base64_encode(encoded, (char *)encrypted, olen);
  return String(encoded); //Can accomodate printable & unprintable characters
}

void loop() {
  // Update NTP time
  timeClient.update();

  // Request temperature from the DS18B20 sensor
  sensors.requestTemperatures();
  temperature = sensors.getTempCByIndex(0);
  temp1 = sensors.getTempCByIndex(1);
  temp2 = sensors.getTempCByIndex(2);

  pH = random(750, 850) / 100.0;
  my_pH = (analogRead(ANALOG_PIN) * (3.3 / 4096.0)) * 3.5;
  Serial.print("pH: ");
  Serial.println(pH);
  Serial.print("Temp: ");
  Serial.println(temperature);
  Serial.print("Temp1: ");
  Serial.println(temp1);
  Serial.print("Temp2: ");
  Serial.println(temp2);


  // Get timestamp
  String timestamp = getCurrentTimestamp();

  // Prepare data in JSON format
  DynamicJsonDocument saveDoc(1024);
  saveDoc["timestamp"] = timestamp;
  saveDoc["temperature"] = temperature;
  saveDoc["temp1"] = temp1;
  saveDoc["temp2"] = temp2;
  saveDoc["ph"] = pH;
  // SaveDoc["uid"] = USER_UID;
  String saveJSONData;
  serializeJson(saveDoc, saveJSONData);

  // Encrypt the data
  String encryptedData = encrypt(saveJSONData);

  String path = "/sensorData/" + USER_UID;

  // Send data to Firebase
  firebase.pushString(path, encryptedData);

  saveDoc.clear();

  // Wait 3 seconds before sending the next reading
  delay(3000);
}
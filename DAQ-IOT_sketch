#include <Arduino.h>
#include "EmonLib.h"
#include "WiFi.h"
#include <driver/adc.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <PubSubClient.h>
#include <SimpleKalmanFilter.h>

//Variaveis de horimetro
unsigned long tempo_referencia = 0;
unsigned long tempo_total_ligado = 0;

/*
 SimpleKalmanFilter(e_mea, e_est, q);
 e_mea: Measurement Uncertainty 
 e_est: Estimation Uncertainty 
 q: Process Noise
 */
// Inicializando o filtro de Kalman
SimpleKalmanFilter simpleKalmanFilter(2, 2, 0.01);

Adafruit_MPU6050 mpu;

// The GPIO pin were the CT sensor is connected to (should be an ADC input)
#define ADC_INPUT_CH1 32 //CH1
#define ADC_INPUT_CH3 34 //CH3
#define ADC_INPUT_CH2 35 //CH2

#define HOME_VOLTAGE 127.0

// Force EmonLib to use 10bit ADC resolution
#define ADC_BITS    10
#define ADC_COUNTS  (1<<ADC_BITS)

// Create instances
EnergyMonitor emon1;
EnergyMonitor emon2;
EnergyMonitor emon3;

// Wifi credentials
const char *WIFI_SSID = "LEONNE";
const char *WIFI_PASSWORD = "Wal475514";
const char* mqtt_server = "192.168.1.100";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

short measurements[30];
short measureIndex = 0;
unsigned long lastMeasurement = 0;
unsigned long timeFinishedSetup = 0;

//base pro calculo de horimetro
unsigned int sec_ = 0;
unsigned int min_ = 0;
unsigned int hrs_ = 0;
unsigned int dias = 0;

void connectToWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.setHostname("esp32-pilot");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Only try 15 times to connect to the WiFi
  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 15){
    delay(500);
    //Serial.print(".");
    retries++;
  }

  // If we still couldn't connect to the WiFi, go to deep sleep for a
  // minute and try again.
  if(WiFi.status() != WL_CONNECTED){
      esp_sleep_enable_timer_wakeup(1 * 60L * 1000000L);
    esp_deep_sleep_start();
  }

    //randomSeed(micros());
  //Serial.println("");
  //Serial.println("WiFi connected");
  //Serial.println("IP address: ");
  //Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    //Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      //Serial.println("connected");
      // Once connected, publish an announcement...
      //client.publish("outTopic", "hello world");
      // ... and resubscribe
      //client.subscribe("inTopic");
    } else {
      //Serial.print("failed, rc=");
      //Serial.print(client.state());
      //Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

double calc_imbalance(double ampsr, double ampss, double ampst) {
  double rs = abs(ampsr - ampss);
  double st = abs(ampss - ampst);
  double rt = abs(ampsr - ampst);
  double dif[] = {rs, st, rt};
  double maximo = dif[0]; // define o valor inicial como o primeiro elemento do array

  for (int i = 1; i < 3; i++) {
    if (dif[i] > maximo) { // compara cada elemento com o valor atual máximo
      maximo = dif[i]; // atualiza o valor máximo
    }
  }
  
  double m = (ampsr+ ampss+ ampst)/3;
  double imbal = (maximo*100)/m;
  
  return imbal;
}

void setup()
{
  adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_11);
  analogReadResolution(10);
  Serial.begin(115200);
  connectToWiFi();
  client.setServer(mqtt_server, 1883);
  // Initialize emon library (channel and calibration number)
  emon1.current(ADC_INPUT_CH1, 291);
  emon2.current(ADC_INPUT_CH2, 291);
  emon3.current(ADC_INPUT_CH3, 291);
  timeFinishedSetup = millis();

  //Setup GY
   // Try to initialize!
  if (!mpu.begin()) {
    //Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  //Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  //Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    //Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    //Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    //Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    //Serial.println("+-16G");
    break;
  }
  
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  //Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    //Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    //Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    //Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    //Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
  //Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    //Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    //Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    //Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    //Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    //Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    //Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    //Serial.println("5 Hz");
    break;
  }

  //Serial.println("");
  delay(100);
}

void loop(){

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long currentMillis = millis();

  // If it's been longer then 1000ms since we took a measurement, take one now!
  if(currentMillis - lastMeasurement > 1000){
    lastMeasurement = millis();
    double ampsR = emon1.calcIrms(1480); // Calculate Irms only fase R
    double ampsS = emon2.calcIrms(1480); // Calculate Irms only fase S
    double ampsT = emon3.calcIrms(1480); // Calculate Irms only fase T
    double wattR = ampsR * HOME_VOLTAGE;
    double wattS = ampsS * HOME_VOLTAGE;
    double wattT = ampsT * HOME_VOLTAGE;
    double imbalance = calc_imbalance(ampsR,ampsS,ampsT);
    String status = "";
    String horimetro = "";

    // Obtendo a estimativa do estado
    float estimated_value = simpleKalmanFilter.updateEstimate(imbalance);

    if (((ampsR+ ampsS+ ampsT)/3) > 0.37) {
      tempo_total_ligado = millis() - tempo_referencia;
      status = "on";
      sec_ = sec_+1;
    }else{
      status = "off";
    }

    // Calcula o tempo ligado em dias, horas e minutos
    unsigned long tempo_ligado = tempo_total_ligado / 1000; // Converte para segundos
    unsigned int segundos = tempo_total_ligado / 1000;
    unsigned int minutos = tempo_ligado / 60;
    unsigned int horas = minutos / 60;
    //unsigned int dias = horas / 24;

    if (sec_ > 59){
      min_ = min_+1;
      sec_ = 0;
    }

    if (min_ > 59){
      hrs_ = hrs_+1;
      min_ = 0;
    }

    if (hrs_ > 23){
      dias = dias+1;
      hrs_ = 0;
    }
    

    horimetro = String(dias) +" dias, "+String(hrs_)+ " hrs "+String(min_)+" min "+String(sec_)+" seg";
    //Serial.print("Current R: ");
    //Serial.println(ampsR);
    //Serial.print("Potência R: ");
    //Serial.println(wattR);

    //Serial.print("Current S: ");
    //Serial.println(ampsS);
    //Serial.print("Potência S: ");
    //Serial.println(wattS);

    //Serial.print("Current T: ");
    //Serial.println(ampsT);
    //Serial.print("Potência T: ");
    //Serial.println(wattT);

/* Get new sensor events with the readings */
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    /* Print out the values */
    //Serial.print("Acceleration X: ");
    //Serial.print(a.acceleration.x);
    //Serial.print(", Y: ");
    //Serial.print(a.acceleration.y);
    //Serial.print(", Z: ");
    //Serial.print(a.acceleration.z);
    //Serial.println(" m/s^2");

    //Serial.print("Rotation X: ");
    //Serial.print(g.gyro.x);
    //Serial.print(", Y: ");
    //Serial.print(g.gyro.y);
    //Serial.print(", Z: ");
    //Serial.print(g.gyro.z);
    //Serial.println(" rad/s");

    //Serial.print("Temperature: ");
    //Serial.print(temp.temperature);
    //Serial.println(" degC");

    //Serial.println("");

    // Convert the value to a char array
    char tempString[8];
    dtostrf(temp.temperature, 1, 2, tempString);
    client.publish("esp32/temperature", tempString);

    char AccXString[18];
    dtostrf(a.acceleration.x, 1, 2, AccXString);
    client.publish("esp32/accelerationX", AccXString);

    char AccYString[8];
    dtostrf(a.acceleration.y, 1, 2, AccYString);
    client.publish("esp32/accelerationY", AccYString);

    char AccZString[8];
    dtostrf(a.acceleration.z, 1, 2, AccZString);
    client.publish("esp32/accelerationZ", AccZString);

    char GyroXString[8];
    dtostrf(g.gyro.x, 1, 2, GyroXString);
    client.publish("esp32/rotationX", GyroXString);

    char GyroYString[8];
    dtostrf(g.gyro.y, 1, 2, GyroYString);
    client.publish("esp32/rotationY", GyroYString);

    char GyroZString[8];
    dtostrf(g.gyro.z, 1, 2, GyroZString);
    client.publish("esp32/rotationZ", GyroZString);

    char ampRString[8];
    dtostrf(ampsR, 1, 2, ampRString);
    client.publish("esp32/current_R", ampRString);

    char ampSString[8];
    dtostrf(ampsS, 1, 2, ampSString);
    client.publish("esp32/current_S", ampSString);

    char ampTString[8];
    dtostrf(ampsT, 1, 2, ampTString);
    client.publish("esp32/current_T", ampTString);

    char wattRString[8];
    dtostrf(wattR, 1, 2, wattRString);
    client.publish("esp32/watt_R", wattRString);

    char wattSString[8];
    dtostrf(wattS, 1, 2, wattSString);
    client.publish("esp32/watt_S", wattSString);

    char wattTString[8];
    dtostrf(wattT, 1, 2, wattTString);
    client.publish("esp32/watt_T", wattTString);

    char imbalanceString[8];
    dtostrf(imbalance, 1, 2, imbalanceString);
    client.publish("esp32/imbalance", imbalanceString);

    char imbalance_estString[8];
    dtostrf(estimated_value, 1, 2, imbalance_estString);
    client.publish("esp32/imbalance_est_kf", imbalance_estString);

    client.publish("esp32/status", status.c_str());

    //char horimetroString[8];
    //dtostrf(horimetro, 1, 2, horimetroString);
    client.publish("esp32/horimetro", horimetro.c_str());

  }
}

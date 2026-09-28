#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Crear objeto del sensor MPU6050
Adafruit_MPU6050 mpu;

// Configuración de la frecuencia de muestreo: 50 Hz (20 ms entre muestras)
const unsigned long SAMPLE_INTERVAL_MS = 20;
unsigned long lastSampleTime = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // Pines I2C para ESP32 (SDA = GPIO 21, SCL = GPIO 22)

  if (!mpu.begin()) {
    Serial.println("Error: No se encontró el módulo MPU6050.");
    while (1) { delay(10); }
  }

  // Configuración de rangos y filtros del sensor
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Imprimir encabezado en formato CSV por el puerto serial
  Serial.println("timestamp_ms,ax,ay,az,gx,gy,gz");
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastSampleTime >= SAMPLE_INTERVAL_MS) {
    lastSampleTime = currentTime;

    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Enviar datos en formato CSV
    Serial.print(currentTime); Serial.print(",");
    Serial.print(a.acceleration.x); Serial.print(",");
    Serial.print(a.acceleration.y); Serial.print(",");
    Serial.print(a.acceleration.z); Serial.print(",");
    Serial.print(g.gyro.x); Serial.print(",");
    Serial.print(g.gyro.y); Serial.print(",");
    Serial.println(g.gyro.z);
  }
}

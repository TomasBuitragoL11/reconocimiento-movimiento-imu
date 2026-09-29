#include <Wire.h>

// Dirección I2C del sensor MPU-6050
const int MPU_ADDR = 0x68;

// Configuración de la frecuencia de muestreo: 50 Hz (20 ms entre muestras)
const unsigned long SAMPLE_INTERVAL_MS = 20;
unsigned long lastSampleTime = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // Pines I2C para ESP32 (SDA = GPIO 21, SCL = GPIO 22)

  // Despertar el MPU-6050 (Escribir 0 en PWR_MGMT_1)
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  // Encabezado CSV por el puerto serial
  Serial.println("timestamp_ms,ax,ay,az,gx,gy,gz");
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastSampleTime >= SAMPLE_INTERVAL_MS) {
    lastSampleTime = currentTime;

    // Solicitar 14 bytes al MPU-6050
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDR, 14, true);

    // Lectura de registros acelerómetro
    int16_t raw_ax = Wire.read() << 8 | Wire.read();
    int16_t raw_ay = Wire.read() << 8 | Wire.read();
    int16_t raw_az = Wire.read() << 8 | Wire.read();
    
    // Ignorar bytes de temperatura
    Wire.read(); Wire.read();

    // Lectura de registros giroscopio
    int16_t raw_gx = Wire.read() << 8 | Wire.read();
    int16_t raw_gy = Wire.read() << 8 | Wire.read();
    int16_t raw_gz = Wire.read() << 8 | Wire.read();

    // Conversión a m/s² y deg/s
    float ax = (raw_ax / 16384.0) * 9.81;
    float ay = (raw_ay / 16384.0) * 9.81;
    float az = (raw_az / 16384.0) * 9.81;
    float gx = raw_gx / 131.0;
    float gy = raw_gy / 131.0;
    float gz = raw_gz / 131.0;

    // Salida por puerto serial
    Serial.print(currentTime); Serial.print(",");
    Serial.print(ax); Serial.print(",");
    Serial.print(ay); Serial.print(",");
    Serial.print(az); Serial.print(",");
    Serial.print(gx); Serial.print(",");
    Serial.print(gy); Serial.print(",");
    Serial.println(gz);
  }
}

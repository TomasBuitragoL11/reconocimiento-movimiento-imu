# Hardware y Simulación del Circuito

## Diagrama de Conexiones (ESP32 + MPU-6050)
El módulo inercial MPU-6050 se conecta al microcontrolador ESP32 mediante el protocolo I2C[cite: 1]:

| Pin MPU-6050 | Pin ESP32 DevKit v1 | Descripción |
| :---: | :---: | :---: |
| **VCC** | **3.3V** | Alimentación principal |
| **GND** | **GND** | Tierra común |
| **SDA** | **GPIO 21** | Línea de Datos I2C |
| **SCL** | **GPIO 22** | Línea de Reloj I2C |

## Simulación del Circuito
El esquemático del circuito y el código del firmware están montados en Wokwi:

**[Abrir Simulación en Wokwi](https://wokwi.com/projects/476428926957185025)** 

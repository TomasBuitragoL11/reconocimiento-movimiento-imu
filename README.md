# reconocimiento-movimiento-imu
Sistema de Reconocimiento de Actividades Humanas (HAR) mediante IMU (MPU-6050), ESP32 y Machine Learning en Python.

## Descripción del Proyecto
Este proyecto implementa un sistema de **Reconocimiento de Actividades Humanas (Human Activity Recognition - HAR)** utilizando una Unidad de Medición Inercial (IMU MPU-6050) y un microcontrolador ESP32. El sistema procesa señales biomecánicas (aceleración y velocidad angular) a 50 Hz para clasificar patrones de movimiento como caminar, correr, sentarse, estar de pie y caídas.

## Estructura del Repositorio
```text
├── docs/               # Documentación teórica y diagramas
├── hardware/           # Esquemáticos y simulaciones (Wokwi)
├── firmware/           # Código C++ para microcontrolador (ESP32/Arduino)
├── data/
│   ├── raw/            # Datos sin procesar (.csv)
│   └── processed/      # Datasets filtrados y segmentados
├── src/                # Código de procesamiento y Machine Learning en Python
├── requirements.txt    # Dependencias de Python
└── README.md           # Descripción del proyecto
```

## Autores
Tomás Buitrago López   
Nicolás Ramírez Ramírez   
Asignatura: Teoría de Señales (C5606001)   
Docente: Mateo Cardona Marín
Institución: Universidad de Manizales

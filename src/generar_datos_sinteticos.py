import os
import numpy as np
import pandas as pd

# Fijar semilla para reproducibilidad
np.random.seed(42)

# Parámetros del dataset
fs = 50  # Frecuencia de muestreo: 50 Hz
duracion_seg = 30  # 30 segundos por actividad
num_muestras = fs * duracion_seg
time = np.linspace(0, duracion_seg, num_muestras)

def generar_actividad(tipo):
    """Genera señales sintetizadas de aceleración y giroscopio para una actividad."""
    # Ruido gaussiano base
    noise_acc = np.random.normal(0, 0.2, (num_muestras, 3))
    noise_gyro = np.random.normal(0, 1.0, (num_muestras, 3))
    
    # Componente estática de gravedad en el eje Z (1g = 9.81 m/s^2)
    g_vector = np.array([0.0, 0.0, 9.81])
    
    if tipo == "estar_de_pie":
        acc = g_vector + noise_acc
        gyro = noise_gyro

    elif tipo == "sentarse":
        # Ligera inclinación constante
        acc = np.array([1.5, 0.0, 9.6]) + noise_acc
        gyro = noise_gyro

    elif tipo == "caminar":
        # Patron sinusoidal ritmico de marcha (~1.5 Hz)
        f_paso = 1.5
        ax = 1.0 * np.sin(2 * np.pi * f_paso * time)
        ay = 0.5 * np.cos(2 * np.pi * f_paso * time)
        az = 9.81 + 2.0 * np.sin(2 * np.pi * 2 * f_paso * time)
        acc = np.column_stack((ax, ay, az)) + noise_acc
        
        gx = 20 * np.sin(2 * np.pi * f_paso * time)
        gy = 10 * np.cos(2 * np.pi * f_paso * time)
        gz = 5 * np.sin(2 * np.pi * f_paso * time)
        gyro = np.column_stack((gx, gy, gz)) + noise_gyro

    elif tipo == "correr":
        # Mayor frecuencia e intensidad (~2.5 Hz)
        f_paso = 2.5
        ax = 2.5 * np.sin(2 * np.pi * f_paso * time)
        ay = 1.2 * np.cos(2 * np.pi * f_paso * time)
        az = 9.81 + 5.0 * np.sin(2 * np.pi * 2 * f_paso * time)
        acc = np.column_stack((ax, ay, az)) + noise_acc * 1.5
        
        gx = 50 * np.sin(2 * np.pi * f_paso * time)
        gy = 25 * np.cos(2 * np.pi * f_paso * time)
        gz = 15 * np.sin(2 * np.pi * f_paso * time)
        gyro = np.column_stack((gx, gy, gz)) + noise_gyro

    elif tipo == "caida":
        # Caida libre (~0g) seguida de un pico brusco de impacto y reposo
        acc = g_vector + noise_acc
        gyro = noise_gyro
        # Evento de caida a los 15 segundos
        idx_caida = int(15 * fs)
        # Caida libre (100 ms)
        acc[idx_caida:idx_caida+5, :] = np.array([0.1, 0.1, 0.5])
        # Impacto (200 ms)
        acc[idx_caida+5:idx_caida+15, :] = np.array([12.0, 15.0, 35.0])
        # Rotación brusca durante el impacto
        gyro[idx_caida+5:idx_caida+15, :] = np.array([180.0, -250.0, 300.0])

    else:
        raise ValueError("Actividad no reconocida")

    df = pd.DataFrame({
        'timestamp_ms': (time * 1000).astype(int),
        'ax': acc[:, 0],
        'ay': acc[:, 1],
        'az': acc[:, 2],
        'gx': gyro[:, 0],
        'gy': gyro[:, 1],
        'gz': gyro[:, 2],
        'actividad': tipo
    })
    return df

if __name__ == "__main__":
    os.makedirs('../data/raw', exist_ok=True)
    actividades = ["estar_de_pie", "sentarse", "caminar", "correr", "caida"]
    
    dfs = []
    for act in actividades:
        df_act = generar_actividad(act)
        dfs.append(df_act)
        # Guardar archivo individual
        df_act.to_csv(f'../data/raw/{act}.csv', index=False)
        print(f"Archivo '../data/raw/{act}.csv' generado.")

    # Guardar dataset combinado
    df_total = pd.concat(dfs, ignore_index=True)
    df_total.to_csv('../data/raw/dataset_completo_raw.csv', index=False)
    print("Dataset completo generado exitosamente en 'data/raw/dataset_completo_raw.csv'.")

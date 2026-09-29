import os
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt

# Parámetros globales de la señal
FS = 50.0          # Frecuencia de muestreo: 50 Hz
CUTOFF = 15.0      # Frecuencia de corte: 15 Hz
WINDOW_SEC = 2.56  # Duración de ventana: 2.56 segundos
OVERLAP = 0.5      # 50% de solapamiento

def butter_lowpass_filter(data, cutoff=CUTOFF, fs=FS, order=4):
    """Aplica un filtro Butterworth pasa-bajas de fase cero (filtfilt)."""
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data, axis=0)
    return filtered_data

def crear_ventanas_deslizantes(df, window_size, step_size):
    """Segmenta las series temporales en ventanas con solapamiento."""
    ventanas = []
    etiquetas = []
    
    canales = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
    
    # Procesar cada actividad por separado para evitar mezclar fronteras
    for actividad, group in df.groupby('actividad'):
        data = group[canales].values
        n_muestras = len(data)
        
        for start in range(0, n_muestras - window_size + 1, step_size):
            end = start + window_size
            ventanas.append(data[start:end])
            etiquetas.append(actividad)
            
    return np.array(ventanas), np.array(etiquetas)

if __name__ == "__main__":
    path_raw = '../data/raw/dataset_completo_raw.csv'
    
    if not os.path.exists(path_raw):
        print(f"Error: No se encontró el archivo {path_raw}. Ejecuta primero 'generar_datos_sinteticos.py'.")
        exit()
        
    df_raw = pd.read_csv(path_raw)
    print(f"Dataset original cargado: {len(df_raw)} muestras.")

    # 1. Aplicar filtro Butterworth a los 6 canales (3 acelerómetro + 3 giroscopio)
    canales = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
    df_filtrado = df_raw.copy()
    df_filtrado[canales] = butter_lowpass_filter(df_raw[canales].values, cutoff=CUTOFF, fs=FS)

    os.makedirs('../data/processed', exist_ok=True)
    df_filtrado.to_csv('../data/processed/dataset_filtrado.csv', index=False)
    print("Filtrado Butterworth completado y guardado en 'data/processed/dataset_filtrado.csv'.")

    # 2. Segmentación en ventanas
    window_size = int(WINDOW_SEC * FS)  # 2.56 s * 50 Hz = 128 muestras
    step_size = int(window_size * (1 - OVERLAP))  # 128 * 0.5 = 64 muestras
    
    X_ventanas, y_etiquetas = crear_ventanas_deslizantes(df_filtrado, window_size, step_size)
    
    print(f"\nSegmentación exitosa:")
    print(f"- Total de ventanas generadas: {X_ventanas.shape[0]}")
    print(f"- Formato de cada ventana (muestras, canales): {X_ventanas.shape[1:]}")
    
    # Guardar arreglos segmentados en formato binario .npy para uso rápido
    np.save('../data/processed/X_ventanas.npy', X_ventanas)
    np.save('../data/processed/y_etiquetas.npy', y_etiquetas)
    print("Ventanas segmentadas guardadas en 'data/processed/'.")

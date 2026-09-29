import os
import numpy as np
import pandas as pd
from scipy.fft import fft
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def extraer_caracteristicas_ventana(ventana):
    """
    Extrae un vector de características (time & frequency domain)
    de una sola ventana de 128 muestras x 6 canales.
    """
    features = []
    
    # Separación de canales (0:ax, 1:ay, 2:az, 3:gx, 4:gy, 5:gz)
    acc = ventana[:, 0:3]
    gyro = ventana[:, 3:6]
    
    # 1. DOMINIO DEL TIEMPO
    # Media y Desviación Estándar por canal
    means = np.mean(ventana, axis=0)
    stds = np.std(ventana, axis=0)
    
    # RMS (Root Mean Square) por canal
    rms = np.sqrt(np.mean(ventana**2, axis=0))
    
    # SMA (Signal Magnitude Area) sobre aceleración: (1/T) * sum(|ax| + |ay| + |az|)
    sma_acc = np.mean(np.sum(np.abs(acc), axis=1))
    
    features.extend(means)
    features.extend(stds)
    features.extend(rms)
    features.append(sma_acc)
    
    # 2. DOMINIO DE LA FRECUENCIA (FFT)
    for ch in range(6):
        signal_ch = ventana[:, ch]
        fft_vals = fft(signal_ch)
        fft_mag = np.abs(fft_vals[:len(signal_ch) // 2])  # Mitad positiva del espectro
        
        # Energía Espectral: Suma de magnitudes al cuadrado
        energia_espectral = np.sum(fft_mag**2) / len(fft_mag)
        
        # Entropía Espectral: Medida de aleatoriedad
        psd = fft_mag**2
        psd_norm = psd / (np.sum(psd) + 1e-12)  # Normalización con eps para evitar div por 0
        entropia_espectral = -np.sum(psd_norm * np.log2(psd_norm + 1e-12))
        
        features.append(energia_espectral)
        features.append(entropia_espectral)
        
    return np.array(features)

def procesar_matriz_caracteristicas(X_ventanas):
    """Recorre todas las ventanas y construye la matriz X de características."""
    X_features = []
    for ventana in X_ventanas:
        feat_vec = extraer_caracteristicas_ventana(ventana)
        X_features.append(feat_vec)
    return np.array(X_features)

if __name__ == "__main__":
    path_X = '../data/processed/X_ventanas.npy'
    path_y = '../data/processed/y_etiquetas.npy'
    
    if not os.path.exists(path_X) or not os.path.exists(path_y):
        print("Error: Arreglos segmentados no encontrados. Ejecuta primero 'preprocesamiento.py'.")
        exit()
        
    X_ventanas = np.load(path_X)
    y = np.load(path_y)
    
    print(f"Cargadas {X_ventanas.shape[0]} ventanas para extracción de características...")
    X = procesar_matriz_caracteristicas(X_ventanas)
    print(f"Matriz de características generada: {X.shape[0]} muestras x {X.shape[1]} características.")
    
    # 3. DIVISIÓN DEL DATASET (70% Entrenamiento, 30% Prueba)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    
    # Escalado de características para SVM
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 4. MODELO 1: RANDOM FOREST
    print("\n" + "="*50)
    print("ENTRENANDO MODELO 1: RANDOM FOREST")
    print("="*50)
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    acc_rf = accuracy_score(y_test, y_pred_rf)
    print(f"Exactitud (Accuracy) Random Forest: {acc_rf * 100:.2f}%\n")
    print("Informe de Clasificación (Random Forest):")
    print(classification_report(y_test, y_pred_rf))
    
    # 5. MODELO 2: SUPPORT VECTOR MACHINE (SVM)
    print("\n" + "="*50)
    print("ENTRENANDO MODELO 2: SUPPORT VECTOR MACHINE (SVM)")
    print("="*50)
    svm_model = SVC(kernel='rbf', C=1.0, random_state=42)
    svm_model.fit(X_train_scaled, y_train)
    y_pred_svm = svm_model.predict(X_test_scaled)
    
    acc_svm = accuracy_score(y_test, y_pred_svm)
    print(f"Exactitud (Accuracy) SVM: {acc_svm * 100:.2f}%\n")
    print("Informe de Clasificación (SVM):")
    print(classification_report(y_test, y_pred_svm))

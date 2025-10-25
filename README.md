# Proyecto: Detección de Phishing con Red de Hamming

## 1. Descripción general
El proyecto combina dos módulos para detectar intentos de **phishing** en correos electrónicos:

1. **Análisis de correos (`main.py`)**: procesa archivos `.txt` con correos, extrae 10 características binarias y genera un dataset `.csv`.
2. **Clasificación (`Nnhamming.py`)**: usa una **Red de Hamming** para clasificar cada correo como `Phishing` o `Legítimo` según los prototipos definidos.

---

## 2. Requisitos
- Python 3.6 o superior
- Librerías necesarias:
  ```bash
  pip install pandas tldextract
  ```

---

## 3. Uso

### Paso 1: Analizar correos
```bash
python main.py correos.txt correos_analizados.csv
```
Genera un archivo `.csv` con 10 características binarias.

### Paso 2: Clasificar con la Red de Hamming
```bash
python Nnhamming.py prototipos.csv correos_analizados.csv --verbose
```
Genera `resultados_clasificacion.csv` con las clases predichas y distancias de Hamming.

---

## 4. Ejemplo de salida
```
📊 REPORTE FINAL DE CLASIFICACIÓN
============================================================
   Phishing    :  39 casos (39.0%)
   Legítimo    :  61 casos (61.0%)
💾 Resultados guardados en: resultados_clasificacion.csv
```

---

## 5. Referencias
[1] Artificial Neural Networks. Edgar Sánchez-Sinencio, Clifford Lau. IEEE Press, 1992.  
[2] Cardinaux, Paredes, Saavedra. *Las Redes de Hamming aplicadas a la detección de phishing*. UADER FCyT, 2025.
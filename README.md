# Proyecto de Detección de Phishing con Red de Hamming

Este proyecto implementa un sistema de detección de intentos de **phishing** en correos electrónicos utilizando una **Red Neuronal de Hamming**. El flujo de trabajo se compone de dos etapas principales:

- **Preprocesamiento de correos**: un script que analiza mensajes y genera un conjunto de características binarias indicadoras de posible phishing.  
- **Clasificación**: una red de Hamming que clasifica los correos procesados según la similitud con prototipos definidos.

## 1. Requisitos de Instalación

Los scripts están desarrollados en **Python 3.6+** y requieren únicamente la librería `pandas` para la etapa de preprocesamiento.

Instálala ejecutando:

```bash
pip install pandas
```

## 2. Flujo de Trabajo

El sistema opera en dos pasos consecutivos: extracción de características y clasificación.

### Paso 1: Análisis de Correos

El script `procesar_correos.py` examina un archivo de texto con correos y genera un **dataset binario** con indicadores de comportamiento típico de *phishing* (por ejemplo, solicitud de información personal o uso de lenguaje promocional).

#### Formato del archivo de entrada

Cada correo debe estar separado por una línea que contenga la palabra exacta `Recibidos`.

#### Uso

```bash
python procesar_correos.py <archivo_entrada.txt> <archivo_salida.csv>
```

**Ejemplo**:
```bash
python procesar_correos.py correos.txt correos_analizados.csv
```

El script generará un archivo CSV con valores 0/1 para cada característica detectada.

### Paso 2: Clasificación con Red de Hamming

El script `Nnhamming.py` clasifica los correos procesados comparando cada registro con prototipos de referencia (por ejemplo, **Phishing** o **Legítimo**) según la **distancia de Hamming**.

#### Archivos requeridos

- **prototipos.csv**: patrones de referencia para cada clase.  
- **dataset.csv**: generado por el paso anterior.

#### Uso

```bash
python Nnhamming.py prototipos.csv dataset.csv
```

**Ejemplo**:
```bash
python Nnhamming.py prototipos.csv correos_analizados.csv
```

El sistema imprimirá la clase asignada y la distancia de Hamming asociada a cada caso.

## 3. Interpretación de Resultados

El clasificador indica para cada correo:
- La **clase asignada** (`Phishing`, `Legítimo` o `Indeterminado`).
- La **distancia de Hamming**, que mide cuántas características difieren del prototipo más cercano.

Una menor distancia implica mayor similitud con el patrón correspondiente.

## 4. Personalización

- **Nuevas características**: puedes ampliar el análisis agregando reglas al script `procesar_correos.py` (por ejemplo, detección de dominios falsos o encabezados falsificados).  
- **Nuevas clases**: añade más filas al archivo `prototipos.csv` si deseas incorporar categorías adicionales (por ejemplo, “Campaña Comercial”, “Correo Interno”).
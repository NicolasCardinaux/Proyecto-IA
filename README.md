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

El sistema funciona en un proceso secuencial y sencillo. A continuación, se detallan los pasos para preprocesar y clasificar tus datos.

### Paso 1: Preprocesamiento de Datos

El script `procesar_correos.py` se encarga de extraer características de un archivo de texto con correos electrónicos y convertirlas en un dataset binario.

#### Formato del archivo de entrada

El archivo de texto de entrada (.txt) debe contener cada correo separado por la línea `Recibidos`.

#### Uso

Utiliza el siguiente comando, reemplazando los nombres de archivo por los que estés usando:

```bash
python procesar_correos.py <archivo_de_entrada.txt> <archivo_de_salida.csv>
```

**Ejemplo**:

```bash
python procesar_correos.py ejemplo.txt ejemplo.csv
```

Este comando leerá `ejemplo.txt` y generará un archivo `ejemplo.csv` con las características binarias de cada correo. Este archivo será la entrada para la siguiente etapa.

### Paso 2: Clasificación con la Red de Hamming

El script `Nnhamming.py` toma los datos preprocesados y los clasifica. El sistema compara cada registro del archivo de entrada con un conjunto de prototipos predefinidos y asigna la clase del prototipo más cercano.

#### Requisitos de archivos

Necesitas dos archivos CSV:

- **Archivo de prototipos**: Debe contener los patrones de referencia para cada clase (ej. `Spam`, `Legitimo`). Se asume que este archivo se llama `prototipos.csv`.
- **Archivo de casos a clasificar**: Es el archivo que generaste en el paso 1 (ej. `ejemplo.csv`).

#### Uso

Ejecuta el siguiente comando, asegurándote de que los archivos existan en la misma carpeta:

```bash
python Nnhamming.py <archivo_de_prototipos.csv> <archivo_de_casos.csv>
```

**Ejemplo**:

```bash
python Nnhamming.py prototipos.csv ejemplo.csv
```

El script imprimirá los resultados de la clasificación directamente en la consola.

#### Salida esperada

Tras la ejecución, verás una tabla con la clase asignada a cada caso, junto con su distancia de Hamming, que representa el número de características diferentes al prototipo más cercano.

## 3. Personalización

Este sistema es flexible y puedes adaptarlo a tus necesidades:

- **Añadir características**: Si deseas que el clasificador considere otras características, simplemente modifica el script `procesar_correos.py` para que las detecte. Luego, añade las nuevas columnas tanto en tu archivo de prototipos como en los datasets que generes.
- **Añadir más prototipos**: Si quieres clasificar en más de dos categorías, simplemente agrega más filas a tu archivo `prototipos.csv`, cada una con una clase diferente.
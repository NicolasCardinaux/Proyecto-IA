# Proyecto de Clasificación con Red de Hamming

Este proyecto es una demostración de un sistema de clasificación de patrones binarios utilizando una Red Neuronal de Hamming. El flujo de trabajo se divide en dos etapas principales, gestionadas por dos scripts de Python:

- **Preprocesamiento de datos**: Un script para transformar datos de texto en un formato binario estructurado (CSV).
- **Clasificación**: Una implementación de la Red de Hamming para clasificar los datos preprocesados.

## 1. Requisitos de Instalación

Ambos scripts están escritos en Python y requieren la librería `pandas` para el procesamiento de archivos CSV. Para preparar tu entorno, abre una terminal y ejecuta el siguiente comando:

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
# Proyecto de Detección de Phishing con Red de Hamming

Este proyecto implementa un sistema de detección de intentos de **phishing** en correos electrónicos utilizando una **Red Neuronal de Hamming**. El flujo de trabajo se compone de dos scripts principales:

1.  **`procesar_correos.py`**: Un pre-procesador que analiza un archivo `.txt` de correos electrónicos y extrae **10 características binarias** (ej. "SolicitaCredenciales", "EnlacesSospechosos") en un archivo `.csv`.
2.  **`Nnhamming.py`**: Un clasificador que utiliza una Red de Hamming para comparar el `.csv` generado contra un archivo de prototipos (`prototipos.csv`) y clasificar cada correo como `Phishing` o `Legitimo`.

-----

## Autores

  * **Cardinaux Nicolás**
  * **Paredes Lorenzo**
  * **Saavedra Nicolás**

**Materia:** Inteligencia Artificial
**Universidad:** UADER - FCyT

-----

## 1\. Requisitos de Instalación

Los scripts están desarrollados en **Python 3.6+**. Las dependencias son diferentes para cada script:

  * **Para `procesar_correos.py` (Análisis) se requiere:**
      * `pandas`
      * `tldextract`
  * **Para `Nnhamming.py` (Clasificación) se requiere:**
      * Ninguna biblioteca externa (solo la biblioteca estándar de Python).

Puedes instalar las dependencias necesarias con:

```bash
pip install pandas tldextract
```

-----

## 2\. Flujo de Trabajo

El sistema opera en dos pasos consecutivos: extracción de características y clasificación.

### Paso 1: Análisis de Correos (`procesar_correos.py`)

Este script lee un archivo de texto plano, separa los correos individuales y genera un `.csv` estructurado con 10 indicadores de phishing.

**Formato del archivo de entrada:**
El script separa los correos buscando líneas que comiencen con:

  * `From:`
  * `De:`
  * `Recibidos`
  * `Received:`

**Uso:**
El script toma el archivo de entrada `.txt` como primer argumento y, opcionalmente, un nombre para el archivo `.csv` de salida.

```bash
python procesar_correos.py <archivo_entrada.txt> [archivo_salida.csv]
```

**Ejemplo Básico** (genera `correos_analizados.csv` por defecto):

```bash
python procesar_correos.py correos.txt
```

**Ejemplo Personalizado** (genera `mi_dataset.csv`):

```bash
python procesar_correos.py correos.txt mi_dataset.csv
```

**Características Extraídas:**

  * `ID`
  * `AsuntoUrgente`
  * `SolicitaCredenciales`
  * `EnlacesSospechosos`
  * `DominioRemitenteSospechoso`
  * `ErroresOrtograficos`
  * `FaltaInformacionContacto`
  * `AmenazasConsecuencias`
  * `PremioInexperado`
  * `ActualizacionUrgente`
  * `SaludoGenerico`

-----

### Paso 2: Clasificación con Red de Hamming (`Nnhamming.py`)

Este script clasifica los correos procesados en el paso anterior. Compara cada fila del `dataset` con los `prototipos` y asigna la clase del prototipo más cercano (con la menor **distancia de Hamming**).

**Archivos requeridos:**

  * **`prototipos.csv`**: Un archivo CSV que define los patrones de referencia para cada clase (ej. `Phishing`, `Legitimo`). Este archivo **debe** tener una columna llamada `Clase`.
  * **`casos.csv`**: El archivo CSV generado en el Paso 1 (ej. `correos_analizados.csv`).

**Ejemplo de formato para `prototipos.csv`:**

```csv
Clase;AsuntoUrgente;SolicitaCredenciales;EnlacesSospechosos;...
Legitimo;0;0;0;...
Legitimo;0;0;1;...
Phishing;1;1;1;...
Phishing;1;0;1;...
```

**Uso:**
El script toma los prototipos y los casos como argumentos posicionales. Acepta argumentos opcionales para ver más detalles y definir la salida.

```bash
python Nnhamming.py <prototipos.csv> <casos.csv> [--verbose] [--salida <archivo.csv>]
```

  * `--verbose`: Muestra la clasificación de cada caso individual en la terminal.
  * `--salida`: Especifica el nombre del archivo CSV de resultados (defecto: `resultados_clasificacion.csv`).

**Ejemplo Básico:**

```bash
python Nnhamming.py prototipos.csv correos_analizados.csv
```

**Ejemplo Avanzado (con más detalles):**

```bash
python Nnhamming.py prototipos.csv correos_analizados.csv --verbose --salida mis_predicciones.csv
```

-----

## 3\. Interpretación de Resultados

El script `Nnhamming.py` imprimirá en la consola un **reporte final** con el conteo y porcentaje de cada clase detectada.

El archivo CSV de salida (ej. `resultados_clasificacion.csv`) contendrá:

  * `ID`: El identificador del correo.
  * `Clase_Predicha`: La clase asignada (`Phishing`, `Legitimo`, etc.).
  * `Distancia_Hamming`: Un número que indica cuántas características difirieron del prototipo ganador. **Una distancia de 0 significa una coincidencia exacta.**

**Manejo de empates:** Si un caso tiene la misma distancia mínima con dos o más clases diferentes, el script asignará la clase del **primer prototipo** que encontró con esa distancia mínima.
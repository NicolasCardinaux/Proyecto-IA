# Manual de Referencia y Guía Técnica: Clasificador de Phishing (`Nnhamming.py`)

Este documento sirve como un manual de usuario completo y una guía técnica detallada para el script `Nnhamming.py`.

## Parte 1: Manual de Usuario (Qué hace y Cómo usarlo)

Esta sección describe el propósito, la instalación y el uso del script desde la perspectiva de un usuario final.

### 1.1. Alcances y Limitaciones

#### Alcances

El programa `Nnhamming.py` implementa una **Red Neuronal de Hamming** para clasificar datos (como correos electrónicos) en categorías predefinidas (ej. **Phishing** o **Legítimos**), basándose en características binarias preprocesadas.

El núcleo de su funcionamiento es asignar la clase del prototipo más cercano en función de la **distancia de Hamming**, que es, simplemente, el número de características que difieren entre un caso de entrada y un prototipo conocido.

**Características principales:**

  * **Clasificación inmediata (Sin Entrenamiento)**: A diferencia de otras redes neuronales, la Red de Hamming no requiere un proceso de "entrenamiento" iterativo. Se configura instantáneamente con los prototipos proporcionados.
  * **Entrada flexible**: Lee archivos CSV y detecta automáticamente el delimitador de columnas (ya sea `;` o `,`), lo que mejora la compatibilidad entre sistemas.
  * **Mapeo robusto a binario**: Convierte automáticamente una amplia gama de valores semánticos (como “sí/no”, “true/false”, “1”/”0”) a un formato binario (`1`/`0`) limpio.
  * **Tolerancia a ruido**: Está diseñado para manejar datos del mundo real. Maneja valores faltantes, vacíos o inválidos (`None`) contándolos como una diferencia (distancia + 1), lo que permite clasificar casos incompletos sin fallar.
  * **Reporte de resultados**: Genera un archivo CSV de salida (ej. `resultados_clasificacion.csv`) claro y conciso con la clasificación, la ID del caso y la distancia de Hamming para cada caso.
  * **Estadísticas en consola**: Muestra un resumen final que informa cuántos casos se clasificaron en cada categoría y su porcentaje, dando una visión general inmediata de los resultados.

#### Limitaciones

  * **Solo Datos Binarios**: El script está diseñado para procesar características que puedan ser mapeadas a **valores binarios (0/1)**. No puede procesar datos numéricos continuos (ej. 0.75) o categóricos no binarios (ej. "Alto", "Medio", "Bajo").
  * **Prototipos Fijos**: No realiza **aprendizaje** ni ajuste automático de prototipos. Los prototipos (los patrones de "Phishing" y "Legítimo") deben ser definidos manualmente por el usuario en `prototipos.csv`. La calidad de la clasificación depende enteramente de la calidad de estos prototipos.
  * **Regla de Empate Simple**: En caso de un **empate** de distancia (donde un caso está exactamente a la misma distancia de dos o más clases diferentes, ej. a 3 de 'Phishing' y a 3 de 'Legítimo'), el script asigna la clase del **primer prototipo** que encontró con esa distancia mínima. Es una regla determinista, pero no necesariamente la más precisa.
  * **Eficiencia**: El script compara cada caso con *todos* los prototipos. Si se usaran miles de prototipos, podría volverse menos eficiente.

### 1.2. Instalación

`Nnhamming.py` es un script autocontenido que utiliza únicamente la **biblioteca estándar de Python**. Esto significa que **no requiere dependencias externas**.

1.  Asegúrese de tener **Python 3.6+** instalado. Puede verificarlo con:
    ```bash
    python3 --version
    ```
2.  Descargue el script `Nnhamming.py` y los archivos CSV (ej. `prototipos.csv`, `casos.csv`) en la misma carpeta.
3.  No requiere ningún paso de instalación adicional (como `pip install`).

### 1.3. Ejecución y Ejemplo Práctico

El script se ejecuta desde la terminal y acepta un conjunto de argumentos para funcionar.

#### Argumentos de la Terminal

  * **`prototipos`**: (Argumento posicional obligatorio) La ruta al archivo CSV que contiene los patrones o prototipos de clasificación (ej. `prototipos.csv`).
  * **`casos`**: (Argumento posicional obligatorio) La ruta al archivo CSV que contiene los datos o casos a clasificar (ej. `casos_a_clasificar.csv`).
  * **`--verbose`**: (Argumento opcional) Si se incluye este "flag", el script mostrará en la consola el resultado de la clasificación para cada caso individualmente, a medida que los procesa.
  * **`--salida`**: (Argumento opcional) Permite especificar un nombre para el archivo CSV de resultados. Si no se proporciona, por defecto se llamará **`resultados_clasificacion.csv`**.

-----

#### Ejemplos de Ejecución

1.  Abre la terminal en la carpeta del proyecto:
    ```bash
    cd ruta/al/proyecto
    ```
2.  **Ejecución Estándar**:
    Clasifica los datos en `casos.csv` usando los patrones de `prototipos.csv` y guarda los resultados en `resultados_clasificacion.csv`.
    ```bash
    python Nnhamming.py prototipos.csv casos.csv
    ```
3.  **Ejecución Detallada (Verbose)**:
    Hace lo mismo, pero imprime cada clasificación en la pantalla y guarda los resultados en un archivo con nombre personalizado.
    ```bash
    python Nnhamming.py prototipos.csv casos.csv --verbose --salida mis_resultados.csv
    ```

#### Salida Esperada (Ejemplo con `--verbose`)

```plaintext
🚀 INICIANDO SISTEMA DE DETECCIÓN DE PHISHING
============================================================
📥 Cargando prototipos de entrenamiento...
✅ Cargados 10 registros desde prototipos.csv
📥 Cargando casos para clasificación...
✅ Cargados 80 registros desde casos.csv
📨 Casos a clasificar: 80
🔧 Características para clasificación: ['AsuntoUrgente', 'SolicitaCredenciales', 'EnlacesSospechosos', 'DominioRemitenteSospechoso', 'ErroresOrtograficos', 'FaltaInformacionContacto', 'AmenazasConsecuencias', 'PremioInexperado', 'ActualizacionUrgente', 'SaludoGenerico']

🔍 INICIANDO CLASIFICACIÓN...
------------------------------------------------------------
✅ Correo01 -> Phishing (distancia: 0)
✅ Correo02 -> Legitimo (distancia: 1)
✅ Correo03 -> Phishing (distancia: 2)
...
✅ Correo80 -> Legitimo (distancia: 3)

📊 REPORTE FINAL DE CLASIFICACIÓN
============================================================
   Phishing    :   40 casos ( 50.0%)
   Legitimo    :   40 casos ( 50.0%)
💾 Resultados guardados en: mis_resultados.csv

✅ PROCESO COMPLETADO EXITOSAMENTE
```

### 1.4. FAQ (Preguntas Frecuentes)

**P1: ¿Por qué se usa una red de Hamming para phishing?**
**R1:** Es una elección excelente porque las características del phishing son inherentemente binarias (ej. "¿pide contraseña?": sí/no, "¿es urgente?": sí/no). La Red de Hamming está diseñada para comparar patrones binarios y encontrar la "coincidencia más cercana" (distancia más baja) sin necesidad de un entrenamiento complejo, lo que la hace rápida, interpretable y fácil de configurar.

**P2: ¿Qué pasa si dos prototipos (uno Phishing y uno Legítimo) tienen la misma distancia mínima?**
**R2:** El script implementa una regla de desempate simple: asignará la clase del **primer prototipo** en el archivo `prototipos.csv` que haya coincidido con esa distancia mínima. Por ejemplo, si un caso está a distancia 3 de 'Phishing' y a distancia 3 de 'Legitimo', y el primer prototipo en su lista era 'Phishing', el caso será clasificado como 'Phishing'.

**P3: ¿Puedo agregar más características o clases?**
**R3:** Sí.

  * **Más Características**: Simplemente añada más columnas en *ambos* archivos (`prototipos.csv` y `casos.csv`). El script las detectará automáticamente.
  * **Más Clases**: Simplemente añada más filas (prototipos) en `prototipos.csv` con nuevas etiquetas en la columna `Clase` (ej. 'Spam', 'Promocion'). El clasificador funcionará perfectamente con múltiples clases.

**P4: ¿Qué pasa si un caso tiene valores inválidos ("xyz") o vacíos?**
**R4:** El script está diseñado para esto. La función `mapear_a_binario` convertirá esos valores en `None`. Luego, la función `calcular_distancia_hamming` interpretará ese `None` como una diferencia (un "mismatch") y sumará 1 a la distancia. Esto es robusto porque trata los datos faltantes o corruptos como una penalización, en lugar de ignorarlos o fallar.

-----

## Parte 2: Guía del Desarrollador (Análisis del Código)

Esta sección explica *cómo* funciona el script `Nnhamming.py` internamente, función por función.

### 2.1. Importaciones y Configuración Global

El script se enorgullece de usar solo bibliotecas estándar de Python, lo que garantiza su portabilidad.

  * `import sys`: Se utiliza para dos propósitos:
    1.  `sys.argv`: Acceder a los argumentos pasados en la línea de comandos.
    2.  `sys.exit(main())`: Para que el script devuelva un código de estado (0 para éxito, 1 para error) al sistema operativo.
  * `import csv`: Fundamental para leer y escribir los archivos de datos. Específicamente, se usa:
      * `csv.DictReader`: Para leer los CSV de entrada como una lista de diccionarios (cada fila es un diccionario `{columna: valor}`).
      * `csv.DictWriter`: Para escribir el archivo de resultados a partir de una lista de diccionarios.
  * `import argparse`: Es la biblioteca estándar para crear interfaces de línea de comandos robustas. Define los argumentos (`prototipos`, `casos`), las opciones (`--verbose`, `--salida`) y genera automáticamente el menú de ayuda (`-h`).
  * `import os`: Se utiliza para una única función crucial: `os.path.exists()`, que permite al script verificar si los archivos de entrada proporcionados por el usuario realmente existen antes de intentar abrirlos.
  * `from typing import ...`: Estas son "sugerencias de tipo" (ej. `List`, `Dict`, `Optional`). No afectan la ejecución, pero mejoran drásticamente la legibilidad del código, indicando qué tipo de datos espera y devuelve cada función.
  * `from collections import Counter`: Una herramienta de la biblioteca de colecciones. Es un diccionario especializado para contar. Lo usamos para generar las estadísticas finales (ej. `{'Phishing': 40, 'Legitimo': 40}`).

### 2.2. La Clase `RedHamming`

Esta clase es el "cerebro" del programa. Contiene toda la lógica de la red neuronal.

#### `def __init__(self, prototipos)` (El Constructor)

  * **Propósito**: Inicializar la red y configurarla con sus patrones.
  * **Acción**: Este método se llama automáticamente cuando se crea una instancia (`red = RedHamming(...)`).
    1.  `self.prototipos = prototipos`: Almacena la lista de diccionarios de prototipos dentro de la instancia de la red. Estos son los patrones que "conoce".
    2.  `self.caracteristicas = self._extraer_caracteristicas_comunes()`: Llama a un método interno para determinar qué columnas del CSV se usarán para la comparación. Esto es crucial, ya que define el "vector de características".
    3.  `print(f"🔧 ...")`: Proporciona retroalimentación inmediata al usuario, mostrándole qué características se han detectado y se utilizarán para la clasificación.

#### `def _extraer_caracteristicas_comunes(self)`

  * **Propósito**: Identificar automáticamente las columnas que contienen características, excluyendo las que son metadatos.
  * **Acción**:
    1.  Asume que todos los prototipos tienen la misma estructura, por lo que solo mira el *primer* prototipo (`self.prototipos[0]`).
    2.  Utiliza una "comprensión de listas" de Python para iterar por todas las claves (nombres de columna) de ese prototipo.
    3.  Filtra y descarta las columnas llamadas `'Clase'` e `'ID'`, ya que no son características de clasificación, sino etiquetas o identificadores.
    4.  Devuelve la lista limpia de nombres de características.

#### `def calcular_distancia_hamming(self, caso, prototipo)`

  * **Propósito**: Calcular la distancia de Hamming (número de bits diferentes) entre un caso y un prototipo. Este es el núcleo matemático de la red.
  * **Acción**:
    1.  Inicia un acumulador: `distancia = 0`.
    2.  Itera sobre la lista de características que la red conoce (`self.caracteristicas`).
    3.  Usa `.get(caracteristica)` para obtener los valores. Esto es más seguro que `dict[caracteristica]` porque devuelve `None` si la característica falta, en lugar de bloquear el programa.
    4.  **Lógica Clave (Tolerancia a Ruido)**: La distancia se incrementa en 1 (`distancia += 1`) si:
          * `valor_caso is None or valor_prototipo is None`: Un valor falta en el caso o en el prototipo. Esto se cuenta como un "mismatch" para penalizar los datos incompletos.
          * `valor_caso != valor_prototipo`: Los valores existen pero son diferentes (ej. `0` vs `1`). Esta es la definición estándar de la distancia de Hamming.

#### `def clasificar(self, caso)`

  * **Propósito**: Asignar una clase a un caso dado, simulando la capa competitiva de una Red de Hamming.
  * **Acción**:
    1.  `caso_filtrado = ...`: Como precaución, filtra el diccionario del caso para asegurarse de que solo contenga características que la red realmente conoce.
    2.  `if not caso_filtrado`: Si el caso no tiene ninguna característica válida, lo clasifica como "Indeterminado" con una distancia de -1.
    3.  `distancias = []`: Inicializa una lista para guardar los resultados de la competencia.
    4.  **Bucle de Competición**: Itera sobre *todos* los prototipos que la red conoce. Por cada uno, llama a `calcular_distancia_hamming` y guarda el resultado como una tupla `(distancia, clase)` en la lista `distancias`.
    5.  `menor_distancia = min(...)`: Encuentra el valor de la distancia más baja en la lista de resultados.
    6.  `votos = Counter(...)`: Esta es la simulación de la "capa competitiva". Filtra la lista `distancias` para incluir solo a aquellos que *empataron* con la `menor_distancia` y los cuenta por clase.
    7.  **Lógica de Desempate**:
          * `if len(votos) > 1`: Comprueba si *más de una clase* obtuvo la puntuación mínima (ej. 'Phishing' y 'Legitimo' ambos con distancia 2).
          * `clase_ganadora = distancias[0][1]`: Si hay empate, aplica la regla simple: elige la clase del primer prototipo en la lista original.
          * `else`: Si no hay empate (un claro ganador), usa `votos.most_common(1)[0][0]` para extraer el nombre de la clase ganadora.
    8.  Devuelve la `clase_ganadora` y la `menor_distancia`.

### 2.3. Funciones Auxiliares (Preparación de Datos)

Estas funciones se ejecutan fuera de la clase y son responsables de la "Extracción, Transformación y Carga" (ETL) de los datos.

#### `def detectar_delimitador(ruta_archivo)`

  * **Propósito**: Mejorar la usabilidad del script al manejar los dos delimitadores CSV más comunes.
  * **Acción**: Abre el archivo (`with open(...)`), lee *solo la primera línea* (`f.readline()`) y comprueba si contiene un punto y coma (`;`). Si lo hace, devuelve `;`. De lo contrario, devuelve `,` como delimitador por defecto.

#### `def mapear_a_binario(valor)`

  * **Propósito**: Función de limpieza de datos más importante. Estandariza la variedad de entradas de "sí" y "no" en `1`, `0` o `None`.
  * **Acción**:
    1.  Maneja celdas vacías (`if valor is None or valor == ''`).
    2.  `valor_str = str(valor).strip().lower()`: Una cadena de limpieza robusta. Convierte el valor a `string`, elimina espacios en blanco al inicio/final (`strip()`) y lo convierte a minúsculas (`lower()`).
    3.  Compara el valor limpio contra un `set` (conjunto) de valores "verdaderos" (ej. `'1', 'true', 'si', 'sí'`). Usar un `set` `{...}` es más rápido para comprobaciones `in` que una `list` `[...]`.
    4.  Hace lo mismo para los valores "falsos".
    5.  `try/except ValueError`: Intenta convertir el valor a `int`. Esto captura `1` y `0` que podrían estar como números.
    6.  `return None`: Si el valor no coincide con ninguna regla (ej. es "xyz"), se considera inválido y se devuelve `None`, que luego será contado como un "mismatch" por la red.

#### `def cargar_datos_csv(ruta, es_prototipos=True)`

  * **Propósito**: Cargar, validar y transformar el contenido de un archivo CSV en una lista de diccionarios Python.
  * **Acción**:
    1.  Llama a `detectar_delimitador` para saber cómo leer el archivo.
    2.  Usa `csv.DictReader` para leer las filas como diccionarios.
    3.  **Validación de Prototipos**: Si `es_prototipos` es `True`, comprueba que la columna `Clase` exista. Si no, imprime un error y retorna `None`, deteniendo el programa.
    4.  Itera sobre cada fila (`enumerate` se usa para obtener el `num_linea` para mensajes de error).
    5.  Crea un `dato_procesado` vacío.
    6.  **Transformación**: Itera sobre las columnas de la fila. Si la columna es `Clase` o `ID`, copia el valor tal cual. Para *todas las demás columnas*, las pasa por `mapear_a_binario` para limpiarlas.
    7.  **Validación de Fila**: Comprueba que los prototipos no tengan un valor de `Clase` vacío.
    8.  Devuelve la lista completa de diccionarios procesados.

### 2.4. `def main()` (La Función Principal)

Esta función es el orquestador que ejecuta todos los pasos en orden.

1.  **Parseo de Argumentos**: Configura y ejecuta `argparse` para leer los argumentos de la línea de comandos (`prototipos`, `casos`, `--verbose`, `--salida`) y almacenarlos en el objeto `args`.
2.  **Validación de Entradas**: Usa `os.path.exists` para comprobar que los archivos `args.prototipos` y `args.casos` existen. Si no, imprime un error y `return 1` (código de error).
3.  **Carga de Datos**: Llama a `cargar_datos_csv` para `prototipos` y `casos`.
4.  **Inicialización de la Red**: Crea la instancia de la red: `red = RedHamming(prototipos)`. Aquí es donde se ejecuta el `__init__` de la clase.
5.  **Bucle de Clasificación**:
      * Prepara una lista vacía `resultados` y un `estadisticas = Counter()`.
      * Itera sobre cada `caso` en la lista `casos`.
      * **Manejo de Errores por Caso**: Envuelve la clasificación de cada caso en un bloque `try...except Exception as e:`. Esto es robusto: si un caso tiene un formato tan corrupto que causa un error, el script lo registra, lo añade a `resultados` como 'Error', y *continúa con el siguiente caso* en lugar de detenerse.
      * **Clasificación**: Llama a `clase_predicha, distancia = red.clasificar(caso)`.
      * **Recolección**: Añade el `{'ID': ..., 'Clase_Predicha': ..., 'Distancia_Hamming': ...}` a la lista `resultados` y actualiza el contador `estadisticas`.
      * **Verbose**: Si `args.verbose` es `True`, imprime la clasificación de esta línea.
6.  **Reporte Final**: Itera sobre `estadisticas.items()` para imprimir el resumen de clasificación en la consola.
7.  **Escritura de Resultados**:
      * Abre el archivo `args.salida` en modo escritura (`'w'`).
      * Obtiene las cabeceras (`campos`) del primer diccionario en `resultados`.
      * Crea un `csv.DictWriter` que sabe cómo mapear los diccionarios a esas cabeceras.
      * `escritor.writeheader()`: Escribe la línea de cabecera (ej. "ID;Clase\_Predicha;...").
      * `escritor.writerows(resultados)`: Escribe eficientemente todas las filas de resultados de una sola vez.
8.  **Salida Exitosa**: Imprime los mensajes finales y `return 0` (código de éxito).

### 2.5. El Bloque `if __name__ == '__main__':`

  * **Propósito**: Es un estándar de Python que permite que un archivo `.py` se comporte de dos maneras.
  * **Acción**:
    1.  Si ejecutas el script directamente (`python Nnhamming.py`), la variable `__name__` es igual a `"__main__"`, por lo que el código dentro del `if` se ejecuta.
    2.  Si *importas* este script desde otro archivo (ej. `import Nnhamming`), `__name__` será `"Nnhamming"`, y el código *no* se ejecutará.
  * `sys.exit(main())`: Llama a la función `main` y pasa su código de retorno (`0` o `1`) a `sys.exit`, lo que permite a otros scripts saber si la ejecución fue exitosa.
**Principales capacidades:**

  * Extracción de 10 indicadores clave de phishing (urgencia, amenazas, enlaces, etc.).
  * Análisis heurístico basado en listas de palabras clave (español/inglés) y expresiones regulares.
  * Análisis de enlaces, incluyendo detección de acortadores y comparación de dominios.
  * Análisis de remitentes para detectar dominios genéricos (ej. `gmail.com`).
  * Generación de un archivo CSV de salida con los resultados.
  * Impresión de un resumen estadístico en consola.

**Limitaciones:**

  * Depende del formato de entrada (separadores como `From:`, `De:`, `Recibidos`).
  * Las reglas son heurísticas; no utiliza aprendizaje automático.
  * Las palabras clave están optimizadas para español e inglés.

-----

### 1.2. Instalación

Requiere Python 3.6+ y las bibliotecas `pandas` y `tldextract`.

1.  Instala las dependencias usando pip:
    ```bash
    pip install pandas tldextract
    ```
2.  Coloca `procesar_correos.py` y tu archivo `.txt` de correos en la misma carpeta.

-----

### 1.3. Uso

El script se ejecuta desde la terminal, tomando el archivo de entrada `.txt` como primer argumento y, opcionalmente, un nombre para el archivo CSV de salida.

#### Básico

Genera `correos_analizados.csv` por defecto.

```bash
python procesar_correos.py correos_entrada.txt
```

#### Personalizado

Guarda el resultado en `mi_dataset.csv`.

```bash
python procesar_correos.py correos_entrada.txt mi_dataset.csv
```

-----

### 1.4. Formato del Archivo de Entrada (.txt)

El script espera un archivo de texto plano que contenga múltiples correos. Intenta separar los correos usando varios delimitadores comunes, como:

  * `\nFrom:`
  * `\nDe:`
  * `\nRecibidos\n`
  * `\nReceived:`

Para un análisis correcto, cada correo individual debe contener cabeceras estándar como `From:` y `Subject:`, seguidas del cuerpo del mensaje.

**Ejemplo de formato esperado:**

```
From: "Banco Seguro" <soporte@bancoseguro-login.com>
Subject: ❗ Acción Requerida: Su cuenta ha sido bloqueada
Estimado cliente,
Detectamos un problema. Verifique su cuenta ahora en http://bit.ly/secure-bank
Si no lo hace, su cuenta será eliminada.
Recibidos
From: "Lucia" <lucia@gmail.com>
Subject: Re: Reunión
Hola equipo,
Nos vemos mañana a las 10.
Saludos.
```

-----

### 1.5. Características Analizadas (.csv)

El script genera un CSV con las siguientes 10 características binarias (`1` = presente, `0` = ausente):

| Columna | Descripción |
| :--- | :--- |
| **ID** | Identificador único (ej. `Correo01`, `Correo02`). |
| **AsuntoUrgente** | El asunto contiene palabras de urgencia (`acción requerida`), exceso de mayúsculas o símbolos (`!!`, `??`). |
| **SolicitaCredenciales** | El cuerpo pide explícitamente `contraseña`, `password`, `iniciar sesión` o `verificar cuenta`. |
| **EnlacesSospechosos** | Detecta acortadores de URL (ej. `bit.ly`) O enlaces cuyo dominio base no coincide con el dominio del remitente. |
| **DominioRemitenteSospechoso** | El remitente usa un dominio genérico (ej. `gmail.com`, `hotmail.com`) o un formato de dominio sospechoso. |
| **ErroresOrtograficos** | Detecta errores comunes de phishing (`nesesita`, `urjente`, `actualisar`) o exceso de signos de exclamación (`!!!`). |
| **FaltaInformacionContacto** | **Ausencia** de información de contacto legítima (teléfono, dirección física o términos corporativos como `Inc.`, `S.A.`). |
| **AmenazasConsecuencias** | El cuerpo usa lenguaje amenazante (`cuenta suspendida`, `pérdida permanente`, `acción legal`, `eliminaremos`). |
| **PremioInexperado** | El cuerpo anuncia un premio falso (`ganador`, `sorteo`, `felicitaciones`, `reclama tu premio`). |
| **ActualizacionUrgente** | El cuerpo solicita una `actualización`, `verificación` o `validación` de información. |
| **SaludoGenerico** | El correo comienza con un saludo impersonal (`Estimado cliente`, `Querido usuario`, `Dear user`). |

-----

### 1.6. Interpretación de Resultados

Cada fila del CSV de salida representa un correo y cada columna una característica binaria (`1` = presente, `0` = ausente).

Adicionalmente, el script imprime un **resumen estadístico** en la consola, mostrando el conteo y porcentaje de cada característica detectada en el lote.

**Salida en consola de ejemplo:**

```plaintext
📈 Resumen de características detectadas:
   AsuntoUrgente: 15/50 (30.0%)
   SolicitaCredenciales: 22/50 (44.0%)
   EnlacesSospechosos: 35/50 (70.0%)
   ...
```

-----

### 1.7. FAQ (Preguntas Frecuentes)

**P1: ¿Qué diferencia tiene respecto a un detector de spam?**
**R1:** Este analizador se centra en patrones de **fraude y suplantación** (solicitud de información, urgencia, remitente falso), no en campañas publicitarias masivas (spam).

**P2: ¿Qué ocurre si el formato del texto no cumple las reglas?**
**R2:** El script intentará analizarlo, pero si no puede extraer cabeceras (como `From:` o `Subject:`) o el formato es muy erróneo, las características pueden marcarse incorrectamente (ej. `0` por defecto).

**P3: ¿Puedo añadir nuevas señales?**
**R3:** Sí. La forma más fácil es editar las listas de palabras clave (ej. `self.URGENTE_KEYWORDS`, `self.CREDENCIALES_KEYWORDS`) dentro del script `procesar_correos.py`.

**P4: ¿Qué idiomas soporta?**
**R4:** Está optimizado principalmente para **español**, con un soporte significativo para **inglés** en la mayoría de las palabras clave.

-----

## Parte 2: Guía del Desarrollador (Análisis del Código)

Esta sección explica *cómo* funciona el script `procesar_correos.py` internamente, componente por componente.

### 2.1. Importaciones y Dependencias

El script importa varios módulos para realizar su trabajo:

  * `import re`: **(Expresiones Regulares)** Esencial para buscar patrones de texto. Se usa para encontrar enlaces, errores ortográficos, saludos, y para dividir el archivo de entrada en correos individuales.
  * `import pandas as pd`: **(Pandas)** Es la biblioteca clave para el manejo de datos. Se utiliza al final para tomar la lista de resultados de Python, estructurarla en un DataFrame (una tabla) y guardarla fácilmente como un archivo CSV (`df.to_csv`).
  * `import sys`: **(Sistema)** Se usa para acceder a los argumentos de la línea de comandos (ej. `sys.argv[1]`, el nombre del archivo de entrada) y para `sys.exit()`.
  * `import os`: **(Sistema Operativo)** Se usa para una validación crucial: `os.path.exists()`, que comprueba si el archivo de entrada proporcionado por el usuario existe antes de intentar abrirlo.
  * `from urllib.parse import urlparse`: **(Análisis de URL)** Una herramienta estándar de Python para descomponer una URL (ej. `http://www.google.com/search`) en sus partes (esquema: `http`, dominio: `www.google.com`, ruta: `/search`).
  * `import tldextract`: **(Extracción de TLD)** Una biblioteca externa *muy* importante. Es más inteligente que `urlparse` para dominios. Sabe que `google.com` es el dominio base de `mail.google.com`, y también que `google.co.uk` es el dominio base de `mail.google.co.uk`. Esto es vital para comparar el dominio del remitente con el dominio de un enlace.

-----

### 2.2. La Clase `PhishingAnalyzer`

Esta clase es el "cerebro" del script. Está diseñada para contener todo el "conocimiento" sobre cómo detectar el phishing.

#### `def __init__(self)` (El Constructor)

Este método se ejecuta automáticamente cuando se crea un `PhishingAnalyzer`. Su único propósito es cargar la "base de conocimiento" del analizador en la memoria.

  * **Listas de Palabras Clave (`self.URGENTE_KEYWORDS`, etc.)**: Define 5 listas de palabras clave (en español e inglés) que se correlacionan fuertemente con tácticas de phishing (Urgencia, Credenciales, Amenazas, Premios, Actualizaciones).
  * **Conjuntos de Dominios (`self.URL_SHORTENERS`, `self.DOMINIOS_GENERICOS`)**: Define dos `sets` (conjuntos). Se usa un `set` en lugar de una `list` porque la comprobación (`if dominio in self.DOMINIOS_GENERICOS`) es mucho más rápida.
      * `URL_SHORTENERS`: Dominios conocidos de acortadores de enlaces (ej. `bit.ly`).
      * `DOMINIOS_GENERICOS`: Dominios de correo público (ej. `gmail.com`). Un banco legítimo no debería enviar alertas desde `banco-soporte@gmail.com`.
  * **Expresiones Regulares (`self.REGEX`)**: Esta es una optimización clave. En lugar de crear la misma expresión regular una y otra vez, `re.compile()` las pre-compila una sola vez al inicio. El diccionario `self.REGEX` almacena estos patrones listos para usar:
      * `errores`: Busca errores ortográficos comunes de phishing.
      * `enlaces`: Busca cualquier texto que parezca una URL.
      * `email`: Busca cualquier texto que parezca una dirección de correo.
      * `saludo_generico`: Busca saludos impersonales *al inicio de una línea*.
      * `telefono`: Busca patrones que parezcan números de teléfono.

-----

### 2.3. Lógica de Extracción de Características

La clase contiene 10 métodos `analizar_...`, uno por cada característica. Cada uno toma una parte del correo (asunto, cuerpo, remitente) y devuelve `1` (característica presente) o `0` (ausente).

  * **Análisis Simple (Palabras Clave)**:

      * `analizar_solicitud_credenciales`, `analizar_amenazas`, `analizar_premio`, `analizar_actualizacion`: Estos son los más simples. Convierten el cuerpo a minúsculas y usan `any(keyword in cuerpo_lower ...)` para ver si alguna de las palabras clave de su lista está presente.
      * `analizar_solicitud_credenciales` es un poco más avanzado, ya que también busca patrones de formulario (ej. "ingrese...contraseña").

  * **Análisis Simple (Regex)**:

      * `analizar_errores`: Comprueba dos cosas: 1) Si la regex `self.REGEX["errores"]` (errores ortográficos) encuentra una coincidencia. 2) Si se encuentran 3 o más signos de exclamación seguidos (`!!!`).
      * `analizar_saludo`: Simplemente comprueba si la regex `self.REGEX["saludo_generico"]` encuentra una coincidencia en el cuerpo.

  * **Análisis Compuesto (Múltiples Factores)**:

      * `analizar_asunto`: Comprueba 3 indicadores en el asunto: 1) Presencia de palabras clave urgentes. 2) Si más del 60% de las letras están en mayúsculas. 3) Si hay símbolos excesivos (ej. `??`, `!!`). Si *alguno* es verdadero, devuelve `1`.

  * **Análisis Invertido (Buscar lo Legítimo)**:

      * `analizar_falta_contacto`: Este método funciona al revés. Busca señales de *legitimidad* (un teléfono, una dirección postal, un término corporativo como `S.A.` o `Inc.`). Si **no encuentra ninguna** de estas señales (`return 0 if ... else 1`), devuelve `1`, indicando que la característica "FaltaInformacionContacto" está presente.

  * **Análisis Complejo (Remitente y Enlaces)**:

      * `analizar_remitente`: Marca `1` (sospechoso) si:
        1.  El email del remitente no se pudo encontrar.
        2.  El dominio del remitente está en la lista de `DOMINIOS_GENERICOS` (ej. `gmail.com`).
        3.  El dominio tiene un formato sospechoso (contiene 4+ números, múltiples guiones, etc.).
      * `analizar_enlaces`: Este es el método más sofisticado.
        1.  Encuentra todos los enlaces en el cuerpo.
        2.  Para cada enlace, comprueba si es un **acortador de URL** (`usa_acortador = 1`).
        3.  Si no es un acortador, usa `tldextract.extract` para obtener el dominio base del enlace (ej. `google.com`) y el dominio base del remitente.
        4.  Si los dominios base **no coinciden**, lo marca como sospechoso (`dominio_sospechoso = 1`).
        5.  La función `analizar_correo` luego combina esto: `1 if (usa_acortador or dominio_sospechoso) else 0`.

-----

### 2.4. Orquestación y Parseo

  * **`def analizar_correo(self, correo_completo, numero_correo)`**:
    Este método es el orquestador de cada correo individual.

    1.  **Parseo Básico**: Intenta dividir el `correo_completo` (un bloque de texto) en `remitente`, `asunto` y `cuerpo` buscando líneas que empiecen con `from:` y `subject:`.
    2.  **Parseo de Remitente**: Utiliza regex para extraer el nombre y el email de la cabecera `From:` (manejando formatos como `"Nombre" <email@dominio.com>`).
    3.  **Llamada a Análisis**: Llama a los 10 métodos `analizar_...` y almacena sus resultados (0 o 1) en un diccionario de `caracteristicas`.
    4.  **Manejo de Errores**: Todo el método está envuelto en un `try...except`. Si el parseo de un correo falla (ej. formato muy corrupto), el `except` captura el error y devuelve un diccionario de características "por defecto" (marcando todo como sospechoso) en lugar de detener el script.

  * **`def procesar_correos_phishing(input_file, output_file)`**:
    Esta es la función principal que maneja el lote de correos.

    1.  **Lectura**: Lee el archivo `.txt` *completo* en una sola variable de texto (`contenido`).
    2.  **División de Correos**: Esta es la parte más crítica. Usa `re.split(patron_separador, contenido)` para dividir el texto gigante en una lista de textos de correos individuales, usando los separadores (como `\nFrom:`, `\nRecibidos\n`) como puntos de corte.
    3.  **Iteración**: Itera sobre la lista de correos y llama a `analyzer.analizar_correo()` para cada uno.
    4.  **Recolección**: Almacena todos los diccionarios de características en una lista llamada `resultados`.
    5.  **Uso de Pandas**:
          * `df = pd.DataFrame(resultados, columns=columnas)`: Convierte la lista de diccionarios en una tabla de Pandas.
          * `df.to_csv(output_file, index=False, ...)`: Guarda esa tabla en el archivo CSV de salida. `index=False` evita que Pandas añada su propia columna de índices.
    6.  **Estadísticas**: Una vez que tiene el DataFrame, calcula las estadísticas (`df[col].sum()`) y las imprime en la consola.

-----

### 2.5. El Bloque `if __name__ == "__main__":`

Este bloque es el punto de entrada cuando ejecutas el script desde la terminal.

1.  **Validación de Argumentos**: Comprueba si el usuario proporcionó al menos un argumento (`len(sys.argv) < 2`).
2.  **Impresión de Ayuda**: Si no hay argumentos, imprime el mensaje de "Uso" (cómo ejecutar el script) y sale.
3.  **Asignación de Variables**: Si hay argumentos, los asigna: `input_file` (obligatorio) y `output_file` (opcional, con un valor por defecto).
4.  **Validación de Archivo**: Usa `os.path.exists(input_file)` para asegurarse de que el archivo de entrada existe antes de hacer nada.
5.  **Ejecución**: Llama a `procesar_correos_phishing(input_file, output_file)` para iniciar todo el proceso.
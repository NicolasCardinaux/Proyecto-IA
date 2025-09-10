# Manual de Referencia: Analizador de Características de Correos (procesar_correos.py)

## 1. Propósito y Alcances

El script `procesar_correos.py` es una herramienta de preprocesamiento diseñada para analizar el contenido de correos electrónicos y extraer características binarias, transformando datos de texto no estructurado en un archivo CSV estructurado. Este dataset puede ser utilizado como entrada para clasificadores como la Red de Hamming (`Nnhamming.py`).  

**Propósito**: Convertir correos electrónicos en un conjunto de características binarias (0s y 1s) para facilitar su análisis o clasificación posterior.  
**Alcances**:  
- **Procesamiento Automático**: Extrae automáticamente características relevantes de correos electrónicos basadas en reglas predefinidas.  
- **Formato Estandarizado**: Genera un archivo CSV compatible con clasificadores como `Nnhamming.py`.  
- **Flexibilidad**: Procesa archivos de texto con múltiples correos, identificando patrones comunes en spam o correos legítimos.  
- **No Clasifica**: Este script no clasifica correos; solo los prepara para clasificación posterior.  

**Limitaciones**:  
- Requiere un formato de entrada específico (separador `Recibidos`).  
- No detecta características avanzadas basadas en aprendizaje automático; utiliza reglas predefinidas.  
- Depende de la calidad del archivo de entrada para generar resultados precisos.

## 2. Proceso de Instalación

El script utiliza la biblioteca `pandas`, que no está incluida en la instalación estándar de Python. Sigue estos pasos para configurarlo:

1. **Instalar Python**: Asegúrate de tener **Python 3.6** o superior. Verifica con:  
   ```bash
   python3 --version
   ```  
   Descarga Python desde [python.org](https://www.python.org) si es necesario.

2. **Instalar pandas**: Instala la biblioteca requerida ejecutando:  
   ```bash
   pip install pandas
   ```

3. **Descargar Archivos**: Coloca el script `procesar_correos.py` y el archivo de entrada (formato `.txt`) en la misma carpeta. Los archivos de ejemplo (como `correos_ejemplo.txt`) pueden ser creados según el formato descrito en la sección 4.

## 3. Modo de Uso

El script se ejecuta desde la línea de comandos, tomando como entrada un archivo de texto con correos y generando un archivo CSV con las características extraídas.

### Uso Básico
```bash
python procesar_correos.py <archivo_de_entrada.txt>
```
**Ejemplo**:  
```bash
python procesar_correos.py mis_correos.txt
```  
**Resultado**: Genera un archivo `correos_analizados.csv` en la misma carpeta.

### Uso Avanzado
Puedes especificar un nombre personalizado para el archivo de salida:  
```bash
python procesar_correos.py <archivo_de_entrada.txt> <archivo_de_salida.csv>
```  
**Ejemplo**:  
```bash
python procesar_correos.py correos_ejemplo.txt resultados_finales.csv
```  
**Resultado**: Genera el archivo `resultados_finales.csv`.

## 4. Formato del Archivo de Entrada (.txt)

El archivo de entrada debe ser un archivo de texto plano donde cada correo esté separado por la línea `Recibidos`. El formato esperado para cada correo es:  

```
Remitente_Nombre <remitente@ejemplo.com>
Asunto del Correo
Cuerpo del correo...
Recibidos
```

**Ejemplo**:  
```
Juan Perez <juan@ejemplo.com>
Oferta Especial: ¡Gana un iPhone!
¡Haz clic ahora y reclama tu premio gratis! Última oportunidad.
Recibidos
Ana Gomez <ana@empresa.com>
Re: Confirmación de reunión
Estimado cliente, gracias por su interés...
Recibidos
```

**Notas**:  
- La línea `Recibidos` debe ser exacta, sin espacios adicionales ni caracteres.  
- Asegúrate de que cada correo tenga un remitente, asunto y cuerpo, aunque el cuerpo puede ser breve.

## 5. Formato del Archivo de Salida (.csv)

El archivo CSV generado contiene un encabezado con los nombres de las características y una fila por cada correo procesado. Las columnas son:  

| **Columna**                  | **Significado (1 = Sí, 0 = No)**                                                                 |
|------------------------------|--------------------------------------------------------------------------------------------------|
| ID                           | Identificador único del correo (generado automáticamente).                                        |
| AsuntoEnMayusculas           | El asunto está en mayúsculas o contiene símbolos excesivos (ej. "¡OFERTA!").                     |
| ContieneOferta               | Incluye palabras clave como "oferta", "gratis" o "premio".                                        |
| UsaLenguajePromocional       | Contiene frases como "descuento", "ahorra" o "promoción".                                        |
| TieneErroresOrtograficos     | Detecta errores ortográficos comunes (basado en reglas simples).                                  |
| SolicitaInfoPersonal         | Solicita datos sensibles (contraseñas, datos bancarios, etc.).                                   |
| ContieneMultiplesLlamadasAccion | Incluye más de 2 llamadas a la acción (ej. "clic aquí", "compra ahora").                       |
| EsUrgente                    | Usa lenguaje de urgencia (ej. "expira pronto", "última oportunidad").                            |
| UsaEmoticonos                | Contiene emoticonos o símbolos gráficos.                                                         |
| EsRespuesta                  | El asunto comienza con "Re:", "Aw:" o similar, indicando una respuesta.                          |
| SaludoGenerico               | Usa saludos genéricos como "Estimado cliente" o "Hola usuario".                                  |
| RemitenteSospechoso          | El nombre del remitente no coincide con el dominio del correo (ej. "Banco XYZ <correo@gmail.com>"). |
| UsaAcortadorURL              | Contiene enlaces con acortadores de URL (ej. bit.ly, tinyurl).                                   |
| ExcesoDeEnlaces              | Contiene una cantidad desproporcionada de enlaces (umbral configurable).                         |

**Ejemplo de CSV**:  
```csv
ID,AsuntoEnMayusculas,ContieneOferta,UsaLenguajePromocional,TieneErroresOrtograficos,SolicitaInfoPersonal,ContieneMultiplesLlamadasAccion,EsUrgente,UsaEmoticonos,EsRespuesta,SaludoGenerico,RemitenteSospechoso,UsaAcortadorURL,ExcesoDeEnlaces
Correo1,1,1,1,0,0,1,1,1,0,0,1,1,0
Correo2,0,0,0,0,0,0,0,0,1,1,0,0,0
```

## 6. Preguntas Frecuentes (FAQ)

**P1: ¿Qué significa un valor 1 o 0 en el CSV?**  
**R1**: Un `1` indica que la característica está presente en el correo; un `0` indica que no lo está.

**P2: ¿El script clasifica los correos como Spam o Legítimo?**  
**R2**: No, `procesar_correos.py` solo extrae características y genera un dataset. La clasificación debe realizarse con otro script, como `Nnhamming.py`, usando el CSV generado.

**P3: ¿Qué pasa si mi archivo de entrada no tiene el formato correcto?**  
**R3**: El script detectará errores como:  
- Falta de la línea `Recibidos` como separador.  
- Correos sin remitente, asunto o cuerpo.  
- Caracteres inesperados en la línea `Recibidos`.  
En estos casos, el script emitirá advertencias y puede omitir correos mal formateados. Revisa los mensajes de error para corregir el archivo.

**P4: ¿Puedo personalizar las características extraídas?**  
**R4**: Sí, pero requiere modificar el código del script para añadir o quitar reglas de detección. Las características actuales están diseñadas para identificar patrones comunes en correos spam.

**P5: ¿El script soporta otros idiomas?**  
**R5**: Las reglas de detección están optimizadas para palabras clave en español (ej. "oferta", "gratis"). Para otros idiomas, deberías ajustar las palabras clave en el código.

## 7. Ejemplo de Integración con Nnhamming.py

1. Usa `procesar_correos.py` para generar un archivo CSV a partir de un archivo de texto con correos:  
   ```bash
   python procesar_correos.py correos_ejemplo.txt dataset_correos.csv
   ```
2. Usa el CSV generado como entrada para `Nnhamming.py`:  
   ```bash
   python Nnhamming.py prototipos_correo.csv dataset_correos.csv
   ```
3. Revisa los resultados de clasificación en la consola.
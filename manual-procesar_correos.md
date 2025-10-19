# Manual de Referencia: Analizador de Características de Phishing (`procesar_correos.py`)

## 1. Propósito y Alcances

El script `procesar_correos.py` analiza el contenido textual de correos electrónicos para detectar **señales de phishing** y las transforma en un **dataset binario estructurado**.  
Su objetivo es facilitar la clasificación de mensajes fraudulentos que buscan obtener credenciales o información personal.  

**Principales capacidades:**
- Extracción automática de características relevantes a intentos de suplantación.  
- Generación de archivos CSV compatibles con clasificadores como `Nnhamming.py`.  
- Enfoque en **comportamientos de engaño**.

**Limitaciones:**
- Depende del formato correcto del archivo (`Recibidos` como separador).  
- Las reglas son heurísticas; no utiliza aprendizaje automático.  
- Está diseñado principalmente para correos en español o inglés.

## 2. Instalación

Requiere Python 3.6+ y la biblioteca `pandas`:

```bash
pip install pandas
```

Coloca `procesar_correos.py` y tu archivo `.txt` de correos en la misma carpeta.

## 3. Uso

### Básico
```bash
python procesar_correos.py correos.txt
```
Genera `correos_analizados.csv`.

### Personalizado
```bash
python procesar_correos.py correos.txt salida.csv
```
Guarda el resultado con el nombre especificado.

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
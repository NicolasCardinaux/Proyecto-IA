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

Cada correo debe estar separado por una línea `Recibidos`.

**Ejemplo**:  
```
Banco Seguro <soporte@bancoseguro.com>
Actualiza tus datos de acceso
Por motivos de seguridad, verifica tu cuenta aquí: bit.ly/secure-login
Recibidos
Oficina RRHH <rrhh@empresa.com>
Re: Confirmación de horario
Gracias por tu respuesta, nos vemos mañana.
Recibidos
```

**Notas**:  
- La línea `Recibidos` debe ser exacta, sin espacios adicionales ni caracteres extra.  
- Cada correo debe contener al menos un remitente, un asunto y un cuerpo, aunque el cuerpo puede ser breve.  
- Si el formato no se respeta, el script omitirá ese correo y mostrará una advertencia en consola.

## 5. Características Analizadas (.csv)

| Columna | Descripción |
|----------|--------------|
| **ID** | Identificador único. |
| **AsuntoEnMayusculas** | Detección de uso excesivo de mayúsculas o signos de alerta. |
| **ContieneOferta** | Busca incentivos falsos ("premio", "gratis", "cupón"). |
| **UsaLenguajePromocional** | Identifica frases persuasivas ("promoción", "exclusivo", "ahorra"). |
| **TieneErroresOrtograficos** | Detecta errores comunes o escritura no profesional. |
| **SolicitaInfoPersonal** | Busca frases como “verifica tu cuenta” o “actualiza tu contraseña”. |
| **ContieneMultiplesLlamadasAccion** | Evalúa la repetición de frases tipo “haz clic aquí” o “regístrate”. |
| **EsUrgente** | Detecta expresiones de urgencia (“última oportunidad”, “expira pronto”). |
| **UsaEmoticonos** | Señala presencia de símbolos o emojis para generar confianza. |
| **EsRespuesta** | Indica si parece una respuesta (prefijo “Re:” o “Fwd:”). |
| **SaludoGenerico** | Saludos impersonales (“Estimado cliente”, “Dear user”). |
| **RemitenteSospechoso** | Verifica inconsistencias entre nombre y dominio (ej. “Banco XYZ <soporte@gmail.com>”). |
| **UsaAcortadorURL** | Detección de servicios como bit.ly o tinyurl. |
| **ExcesoDeEnlaces** | Marca si la cantidad de enlaces supera un umbral razonable. |

## 6. Interpretación de Resultados

Cada fila representa un correo y cada columna una característica binaria:
- **1**: presente  
- **0**: ausente  

El CSV resultante puede ser clasificado con `Nnhamming.py` para determinar si el correo es **Phishing** o **Legítimo**.

## 7. Preguntas Frecuentes (FAQ)

**P1:** ¿Qué diferencia tiene respecto a un detector de spam?  
**R1:** Este analizador se centra en patrones de **fraude y suplantación** (solicitud de información, urgencia, remitente falso), no en campañas publicitarias.

**P2:** ¿Qué ocurre si el formato del texto no cumple las reglas?  
**R2:** Los correos mal estructurados se omiten con una advertencia en consola.

**P3:** ¿Puedo añadir nuevas señales?  
**R3:** Sí, editando las listas de palabras clave o funciones de detección dentro del script.

**P4:** ¿Qué idiomas soporta?  
**R4:** Está optimizado para español, con soporte parcial para inglés.

## 8. Integración con Nnhamming.py

1. Analiza tus correos:
   ```bash
   python procesar_correos.py correos.txt dataset.csv
   ```
2. Clasifica los resultados:
   ```bash
   python Nnhamming.py prototipos.csv dataset.csv
   ```
3. Revisa las predicciones en la consola o en el archivo de log.
# Manual de Referencia: Clasificador de Phishing con Red de Hamming (`Nnhamming.py`)

## 1. Alcances y Limitaciones

### Alcances
El programa `Nnhamming.py` implementa una **Red Neuronal de Hamming** para clasificar correos electrónicos como **Phishing** o **Legítimos**, a partir de características binarias preprocesadas.

Se basa en una capa competitiva con **inhibición lateral simulada**, asignando la clase del prototipo más cercano en función de la **distancia de Hamming**.

**Características principales:**
- **Clasificación inmediata**: no requiere entrenamiento.  
- **Entrada flexible**: lectura automática de archivos CSV con detección de delimitador (`;` o `,`).  
- **Validación de consistencia** mediante metadatos opcionales.  
- **Tolerancia a ruido**: clasifica incluso con diferencias parciales respecto al prototipo.  
- **Gestión de errores y logs**: detalla inconsistencias en datos o formato.  
- **Interpretabilidad**: muestra clase asignada y distancia de Hamming por caso.


### Limitaciones
- Solo acepta **valores binarios (0/1)** o equivalentes semánticos (“sí/no”, “true/false”).  
- No realiza **aprendizaje** ni ajuste automático de prototipos.  
- En caso de empate de distancia, asigna la clase **“Indeterminado”**.  
- Puede ser menos eficiente con un número muy elevado de prototipos.

## 2. Instalación

`Nnhamming.py` utiliza únicamente la **biblioteca estándar de Python**, sin dependencias externas.

1. Verifica tu versión, debe ser **Python 3.6+**:
   ```bash
   python3 --version
   ```
2. Descarga el script y los archivos CSV (`prototipos.csv`, `dataset.csv`).  
3. No requiere instalación adicional.

## 3. Ejecución y Ejemplo Práctico

1. Abre la terminal en la carpeta del proyecto:
   ```bash
   cd ruta/al/proyecto
   ```
2. Ejecuta el clasificador:
   ```bash
   python Nnhamming.py prototipos.csv dataset.csv
   ```
3. Opcionalmente agrega parámetros:
   ```bash
   python Nnhamming.py prototipos.csv dataset.csv --log resultados.log --verbose
   ```

**Salida esperada:**
```plaintext
--- INICIO DE CLASIFICACIÓN CON RED DE HAMMING ---
Prototipos: ['Phishing', 'Legitimo']
Características: 10 -> [...]
------------------------------------------------------------
  > Caso 'email_01': Clasificado como 'Phishing' (Hamming=2)
  > Caso 'email_02': Clasificado como 'Legitimo' (Hamming=1)
------------------------------------------------------------
--- CLASIFICACIÓN FINALIZADA ---
```

## 4. FAQ (Preguntas Frecuentes)

**P1: ¿Qué sucede si un caso tiene la misma distancia de Hamming a dos prototipos?**  
**R1**: Si un caso tiene la misma distancia mínima a dos prototipos, se asigna la clase “Indeterminado”. De esta forma, el sistema no resuelve la ambigüedad a favor de ninguna clase en particular y evita clasificaciones erróneas cuando los patrones son indistinguibles.

**P2: ¿Puedo agregar más características para analizar los correos?**  
**R2**: Sí, puedes añadir o eliminar columnas en los archivos CSV de prototipos y casos, siempre que los encabezados coincidan en ambos archivos y estén definidos en `prototipos.csv` (si se usa). El script detecta automáticamente las características.

**P3: ¿Por qué mi archivo CSV genera un error de formato?**  
**R3**: Los errores comunes incluyen:  
- Nombres de columnas diferentes entre `prototipos_correo.csv` y `dataset_base.csv`.  
- Valores no binarios (ej. "3" en lugar de "0" o "1").  
- Falta de encabezado en la primera fila del CSV.  
- Delimitadores inconsistentes (usa `,` o `;` consistentemente).  
- Columnas no definidas en `prototipos.csv` (si se usa).  
Revisa los mensajes de error en la consola o el archivo de log para detalles específicos.

**P4: ¿Puedo usar valores no numéricos como 'yes'/'no'?**  
**R4**: Sí, el script mapea automáticamente valores como 'yes'/'no', 'true'/'false', 'sí'/'no', etc., a 0 y 1. Otros valores (ej. texto arbitrario) causarán un error.

**P5: ¿Para qué sirve el archivo de prototipos?**  
**R5**: El archivo `prototipos.csv`  especifica las características esperadas y su tipo (binario). Ayuda a validar que las columnas en los archivos CSV sean correctas y consistentes.

**P6: ¿Cómo funciona el archivo de log?**  
**R6**: Si especificas `--log errores.log`, los mensajes de error y los resultados de clasificación se guardan en el archivo con marca de tiempo. Esto es útil para depurar o auditar el proceso.

## 5. Referencias
[1] Artificial Neural Networks. Edgar Sánchez-Sinencio and Clifford Lau. IEEE Press. 1992.  
[2] Presentación "Las Redes de Hamming" - Cradinaux, Paredes, Saavedra. UADER 2025.

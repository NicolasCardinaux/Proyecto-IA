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

## 3. Modo de Correr un Test Demo

Para probar el funcionamiento del clasificador:

1. Abre una terminal o consola de comandos.
2. Navega a la carpeta con los archivos usando:
   ```bash
   cd ruta/a/tu/carpeta
   ```
3. Ejecuta el script con los archivos de prototipos y casos:
   ```bash
   python Nnhamming.py prototipos_correo.csv dataset_base.csv
   ```
   O con opciones adicionales:
   ```bash
   python Nnhamming.py prototipos_correo.csv dataset_base.csv --prototipos prototipos.csv --log errores.log --verbose
   ```
4. **Salida Esperada**: El programa mostrará la clasificación de cada caso en `dataset_base.csv`, indicando el ID del caso, la clase asignada (ej. Spam o Legítimo), y la distancia de Hamming al prototipo más cercano. Los errores y resultados se registran en `errores.log` si se especifica `--log`.
5. **Ayuda Adicional**: Para ver un manual de uso detallado, ejecuta:
   ```bash
   python Nnhamming.py --help
   ```

### Ejemplo de Archivos CSV
- **prototipos_correo.csv**:
  ```csv
  Clase,Caracteristica1,Caracteristica2,Caracteristica3,Caracteristica4
  Spam,1,0,1,0
  Legitimo,0,1,0,1
  ```
- **dataset_base.csv**:
  ```csv
  ID,Caracteristica1,Caracteristica2,Caracteristica3,Caracteristica4
  Caso1,1,0,1,1
  Caso2,0,1,0,0
  ```
- **prototipos.csv** (opcional):
  ```csv
  Caracteristica,Tipo
  Caracteristica1,binario
  Caracteristica2,binario
  Caracteristica3,binario
  Caracteristica4,binario
  ```

### Ejemplo de Salida
```plaintext
--- INICIO DE CLASIFICACIÓN CON RED DE HAMMING ---
Prototipos: ['Spam', 'Legitimo']
Características: 4 -> ['Caracteristica1', 'Caracteristica2', 'Caracteristica3', 'Caracteristica4']
------------------------------------------------------------
  > Caso 'Caso1': Clasificado como 'Spam' (Hamming=1)
  > Caso 'Caso2': Clasificado como 'Legitimo' (Hamming=1)
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

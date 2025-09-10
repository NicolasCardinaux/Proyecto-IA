# Manual de Referencia: Clasificador de Spam con Red de Hamming (Nnhamming.py)

## 1. Alcances y Limitaciones

### Alcances
El programa `Nnhamming.py` implementa una **Red Neuronal de Hamming** para clasificar patrones binarios, diseñada específicamente para clasificar correos electrónicos como **Spam** o **Legítimo** basándose en características binarias (0s y 1s). Utiliza una capa competitiva con inhibición lateral simulada para asignar la clase del prototipo más cercano según la **distancia de Hamming**.

- **Clasificación Instantánea**: No requiere entrenamiento, permitiendo clasificaciones rápidas y eficientes, ideal para aplicaciones en tiempo real [1, 2].
- **Entrada Flexible por CSV**: Soporta archivos CSV para prototipos y casos, con detección automática de delimitadores (`,` o `;`) y validación de encabezados.
- **Soporte para Metadatos**: Permite un archivo CSV opcional (`metadata.csv`) para especificar las características esperadas y sus tipos (binario), mejorando la validación.
- **Robustez al Ruido**: Tolera pequeñas variaciones en los patrones de entrada, asignando casos al prototipo más cercano incluso si no hay coincidencia exacta [1].
- **Manejo Avanzado de Errores**: Valida archivos, codificación, y valores binarios, con mensajes detallados y registro opcional en un archivo de log.
- **Salida Detallada**: Proporciona información sobre la clasificación, incluyendo la distancia de Hamming y la clase asignada, con soporte para modo verbose.
- **Manual Integrado**: El argumento `--help` ofrece un manual completo con ejemplos de uso.

### Limitaciones
- **Solo Datos Binarios**: Solo procesa características binarias (0/1 o equivalentes como 'yes'/'no', 'true'/'false'). Datos no binarios requieren preprocesamiento [1].
- **Sin Aprendizaje**: La red no ajusta prototipos automáticamente; cualquier cambio en las clases requiere modificar manualmente el archivo de prototipos.
- **Escalabilidad Limitada**: El rendimiento puede degradarse con un número muy grande de prototipos, ya que compara cada caso con todos los prototipos [1].
- **Empates en Distancia**: En caso de empate en la distancia de Hamming, asigna la clase "Indeterminado" para evitar sesgos, lo que puede requerir intervención manual para resolver ambigüedades.

## 2. Proceso de Instalación

La instalación es sencilla, ya que `Nnhamming.py` utiliza únicamente la biblioteca estándar de Python.

1. **Requisito de Python**: Asegúrate de tener **Python 3.6** o superior instalado. Verifica con:
   ```bash
   python3 --version
   ```
2. **Descarga de Archivos**: Coloca el script `Nnhamming.py`, los archivos CSV de ejemplo (`prototipos_correo.csv`, `dataset_base.csv`), y opcionalmente `metadata.csv` en una misma carpeta.
3. **Sin Dependencias Externas**: No se requiere instalar paquetes adicionales con `pip`. El script está listo para ejecutarse.
4. **Opcional**: Consulta el archivo `README.md` (si se incluye) para instrucciones detalladas y ejemplos de archivos CSV.

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
   python Nnhamming.py prototipos_correo.csv dataset_base.csv --metadata metadata.csv --log errores.log --verbose
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
- **metadata.csv** (opcional):
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
**R1**: Si un caso tiene la misma distancia mínima a dos prototipos, se asigna la clase “Spam”, asegurando que los casos ambiguos se consideren potencialmente peligrosos o no deseados. Esto evita que el sistema subestime correos de riesgo y simplifica la decisión ante empates.

**P2: ¿Puedo agregar más características para analizar los correos?**  
**R2**: Sí, puedes añadir o eliminar columnas en los archivos CSV de prototipos y casos, siempre que los encabezados coincidan en ambos archivos y estén definidos en `metadata.csv` (si se usa). El script detecta automáticamente las características.

**P3: ¿Por qué mi archivo CSV genera un error de formato?**  
**R3**: Los errores comunes incluyen:  
- Nombres de columnas diferentes entre `prototipos_correo.csv` y `dataset_base.csv`.  
- Valores no binarios (ej. "3" en lugar de "0" o "1").  
- Falta de encabezado en la primera fila del CSV.  
- Delimitadores inconsistentes (usa `,` o `;` consistentemente).  
- Columnas no definidas en `metadata.csv` (si se usa).  
Revisa los mensajes de error en la consola o el archivo de log para detalles específicos.

**P4: ¿Puedo usar valores no numéricos como 'yes'/'no'?**  
**R4**: Sí, el script mapea automáticamente valores como 'yes'/'no', 'true'/'false', 'sí'/'no', etc., a 0 y 1. Otros valores (ej. texto arbitrario) causarán un error.

**P5: ¿Para qué sirve el archivo de metadatos?**  
**R5**: El archivo `metadata.csv` (opcional) especifica las características esperadas y su tipo (binario). Ayuda a validar que las columnas en los archivos CSV sean correctas y consistentes.

**P6: ¿Cómo funciona el archivo de log?**  
**R6**: Si especificas `--log errores.log`, los mensajes de error y los resultados de clasificación se guardan en el archivo con marca de tiempo. Esto es útil para depurar o auditar el proceso.

## 5. Referencias
[1] Artificial Neural Networks. Edgar Sánchez-Sinencio and Clifford Lau. IEEE Press. 1992.  
[2] Presentación "Las Redes de Hamming" - Cradinaux, Paredez, Saavedra. UADER 2025.
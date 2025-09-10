# Manual de Referencia: Clasificador de Spam con Red de Hamming (Nnhamming.py)

## 1. Alcances y Limitaciones

### Alcances
El programa `Nnhamming.py` es una implementación de una Red Neuronal de Hamming diseñada para la **clasificación de patrones binarios**. Su principal objetivo es tomar un conjunto de datos (correos) representados por características binarias (1s y 0s) y determinar a cuál de los **prototipos predefinidos** (`Spam` o `Legitimo`) se parece más.

- [cite_start]**Clasificación Rápida**: La principal fortaleza del sistema es su velocidad[cite: 97, 40]. No hay un proceso de "entrenamiento", la clasificación es casi instantánea.
- **Entrada por CSV**: El sistema es flexible y permite al usuario definir sus propios prototipos y casos de prueba a través de archivos CSV.
- [cite_start]**Robustez al Ruido**: Tolera pequeñas diferencias en los patrones de entrada, clasificando un caso en la categoría más cercana aunque no sea una coincidencia perfecta[cite: 105, 39].

### Limitaciones
- [cite_start]**Solo Datos Binarios**: El sistema solo puede procesar datos que sean estrictamente binarios (0 o 1)[cite: 109]. Cualquier otro tipo de dato debe ser pre-procesado.
- **No Aprende**: La red no aprende de nuevos datos. Para añadir o modificar una categoría, se debe editar manualmente el archivo de prototipos.
- [cite_start]**Escalabilidad Limitada**: El rendimiento puede disminuir si el número de prototipos (clases) aumenta considerablemente, ya que cada caso debe ser comparado contra cada prototipo[cite: 112].

## 2. Proceso de Instalación

La instalación es muy sencilla gracias a que el script solo utiliza librerías estándar de Python.

1.  **Tener Python**: Asegúrate de tener Python 3.6 o una versión superior instalada en tu sistema. Puedes verificarlo abriendo una terminal y escribiendo `python3 --version`.
2.  **Descargar los Archivos**: Descarga el script `Nnhamming.py` y los archivos CSV de ejemplo (`prototipos_correo.csv`, `dataset_base.csv`, etc.) en una misma carpeta.
3.  **No se requieren dependencias**: No es necesario instalar paquetes adicionales con `pip`. El script está listo para ser ejecutado.

## 3. Modo de Correr un Test Demo

Para realizar una prueba rápida y verificar que todo funciona correctamente:

1.  Abre una terminal o consola de comandos.
2.  Navega hasta la carpeta donde guardaste los archivos usando el comando `cd ruta/a/tu/carpeta`.
3.  Ejecuta el siguiente comando:
    ```bash
    python Nnhamming.py prototipos_correo.csv dataset_base.csv
    ```
4.  **Salida Esperada**: Deberías ver en la pantalla el resultado de la clasificación para cada correo en el archivo `dataset_base.csv`, indicando su clase asignada y su distancia de Hamming.

## 4. FAQ (Preguntas Frecuentes)

**P1: ¿Qué sucede si un correo tiene la misma distancia a 'Spam' y a 'Legitimo'?**
**R1:** El algoritmo actual asignará la clase del primer prototipo que encuentre en el archivo `prototipos_correo.csv` que cumpla con esa distancia mínima. En nuestro caso, si 'Spam' está primero, se clasificaría como 'Spam' en caso de empate.

**P2: ¿Puedo agregar más características para analizar los correos?**
**R2:** Sí. Para hacerlo, debes agregar la nueva columna tanto en el archivo de prototipos como en los archivos de datasets. El script detectará automáticamente la nueva característica y la incluirá en el cálculo de la distancia, siempre y cuando los encabezados coincidan.

**P3: ¿Por qué mi archivo CSV da un error de formato?**
**R3:** La causa más común es que el número o los nombres de las columnas en tu archivo de casos no coinciden exactamente con los del archivo de prototipos. Asegúrate de que todos los archivos tengan las mismas 11 columnas (1 de ID/Clase y 10 de características) con los mismos nombres.

## 5. REFERENCIAS
[1] Artificial Neural Networks. Edgar Sánchez-Sinencio and Clifford Lau. IEEE Press. 1992.
[2] Presentación "Las Redes de Hamming" - Cradinaux, Paredez, Saavedra. UADER 2025.
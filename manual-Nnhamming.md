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

**P1:** ¿Por qué se usa una red de Hamming para phishing?  
**R1:** Porque permite comparar directamente la estructura binaria de correos con patrones típicos de suplantación (pedidos de credenciales, URLs acortadas, urgencia artificial) sin necesidad de entrenamiento previo.

**P2:** ¿Qué pasa si dos prototipos tienen igual distancia?  
**R2:** Se asigna la clase *Indeterminado* para evitar sesgos.

**P3:** ¿Puedo agregar más características o clases?  
**R3:** Sí. Añade columnas y filas en los CSV asegurando que las cabeceras coincidan.

**P4:** ¿Por qué algunos correos quedan sin clasificar?  
**R4:** Ocurre si poseen valores inválidos o vacíos. El programa los registra como errores o los marca como “Indeterminado”.

**P5:** ¿Qué diferencia hay con un detector de spam?  
**R5:** Este clasificador se centra en indicadores de **suplantación de identidad** (dominios falsos, enlaces engañosos, urgencia y solicitudes de datos), no en promociones masivas o publicidad.

## 5. Referencias
[1] Artificial Neural Networks. Edgar Sánchez-Sinencio, Clifford Lau. IEEE Press, 1992.  
[2] Cardinaux, Paredes, Saavedra. *Las Redes de Hamming aplicadas a la detección de phishing*. UADER FCyT, 2025.

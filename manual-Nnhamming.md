## Clasificador Red de Hamming (`Nnhamming.py`)

## 1. Descripción
Implementa una **Red de Hamming** que compara cada caso con prototipos definidos y clasifica los correos en `Phishing` o `Legítimos` según la **distancia de Hamming** (cantidad de diferencias entre vectores binarios).

---

## 2. Requisitos
- Python 3.6+
- No requiere librerías externas.

Archivos requeridos:
- `prototipos.csv`: define las clases y patrones de referencia.
- `correos_analizados.csv`: dataset generado por el analizador.

---

## 3. Uso
```bash
python Nnhamming.py prototipos.csv correos_analizados.csv --verbose
```
**Opciones:**
- `--verbose`: muestra cada clasificación.
- `--salida <nombre.csv>`: define nombre del archivo de resultados.
---

## 4. Ejemplo de salida
```
📊 REPORTE FINAL DE CLASIFICACIÓN
============================================================
   Phishing    :  50 casos (50.0%)
   Legítimo    :  50 casos (50.0%)
💾 Resultados guardados en: resultados_clasificacion.csv
✅ PROCESO COMPLETADO EXITOSAMENTE
```

---

## 5. FAQ

**P1:** ¿Qué pasa si un caso tiene la misma distancia con dos clases?  
**R1:** El programa asigna la clase del primer prototipo que aparece en el archivo.

**P2:** ¿Puedo agregar más características?  
**R2:** Sí, siempre que se agreguen las mismas columnas a prototipos y casos.

**P3:** ¿Qué significa una distancia alta?  
**R3:** Indica que el caso es muy distinto a todos los prototipos conocidos; la clasificación es menos confiable.

---

## 6. Referencias
[1] Artificial Neural Networks. Edgar Sánchez-Sinencio, Clifford Lau. IEEE Press, 1992.  
[2] Cardinaux, Paredes, Saavedra. *Las Redes de Hamming aplicadas a la detección de phishing*. UADER FCyT, 2025.

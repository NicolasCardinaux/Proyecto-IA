## Clasificador Red de Hamming (`Nnhamming.py`)

## 1. Descripción general
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
   Phishing    :  39 casos (39.0%)
   Legítimo    :  61 casos (61.0%)
💾 Resultados guardados en: resultados_clasificacion.csv
✅ PROCESO COMPLETADO EXITOSAMENTE
```

---

## 5. Referencias
[1] Artificial Neural Networks. Edgar Sánchez-Sinencio, Clifford Lau. IEEE Press, 1992.  
[2] Cardinaux, Paredes, Saavedra. *Las Redes de Hamming aplicadas a la detección de phishing*. UADER FCyT, 2025.
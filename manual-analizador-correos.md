# Analizador de Correos Phishing (`main.py`)

## 1. Descripción general
Lee un archivo `.txt` con correos electrónicos y genera un `.csv` con **10 indicadores binarios** de phishing. Cada fila representa un correo y cada columna una característica detectada.

---

## 2. Requisitos
- Python 3.6+
- Librerías: `pandas`, `tldextract`
  ```bash
  pip install pandas tldextract
  ```

---

## 3. Uso
```bash
python main.py correos.txt correos_analizados.csv
```

**Entradas:**
- `correos.txt`: archivo con varios correos.

**Salida:**
- `correos_analizados.csv`: tabla con 10 columnas binarias.

---

## 4. Ejemplo de salida
| ID | AsuntoUrgente | SolicitaCredenciales | EnlacesSospechosos | DominioRemitenteSospechoso | ... |
|----|----------------|----------------------|--------------------|-----------------------------|-----|
| Correo01 | 1 | 1 | 1 | 0 | ... |
| Correo02 | 0 | 0 | 0 | 1 | ... |

**Resumen en consola:**
```
✅ Análisis completado! Resultados guardados en: correos_analizados.csv
```

---

## 5. Referencias
[1] Artificial Neural Networks. Edgar Sánchez-Sinencio, Clifford Lau. IEEE Press, 1992.  
[2] Cardinaux, Paredes, Saavedra. *Las Redes de Hamming aplicadas a la detección de phishing*. UADER FCyT, 2025.

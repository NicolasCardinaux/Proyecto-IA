import csv
from typing import List, Dict, Optional

def mapear_a_binario(valor: str) -> Optional[int]:
    """Convierte un valor a binario (0/1) de forma robusta."""
    if valor is None or valor == '':
        return None
        
    valor_str = str(valor).strip().lower()
    
    if valor_str in {'1', 'true', 'verdadero', 'si', 'sí', 'yes', 'y', 't', 'v'}:
        return 1
        
    if valor_str in {'0', 'false', 'falso', 'no', 'n', 'f'}:
        return 0
        
    try:
        num = int(valor_str)
        return 1 if num == 1 else 0 if num == 0 else None
    except ValueError:
        return None

def detectar_delimitador(ruta_archivo: str) -> str:
    """Detecta automáticamente el delimitador del CSV."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            primera_linea = f.readline().strip()
            if ';' in primera_linea:
                return ';'
            elif ',' in primera_linea:
                return ','
            else:
                return ','  # Por defecto
    except Exception as e:
        raise ValueError(f"No se pudo detectar delimitador: {e}")

def cargar_datos_csv(ruta: str, es_prototipos: bool = True) -> Optional[List[Dict]]:
    """Carga datos desde archivo CSV con validación."""
    try:
        delim = detectar_delimitador(ruta)
        
        with open(ruta, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f, delimiter=delim)
            if lector.fieldnames is None:
                print(f"❌ ERROR: Archivo vacío o sin encabezados: {ruta}")
                return None
                
            campos = [campo.strip() for campo in lector.fieldnames]
            
            if es_prototipos and 'Clase' not in campos:
                print("❌ ERROR: Los prototipos deben incluir columna 'Clase'")
                return None
                
            datos = []
            
            for num_linea, fila in enumerate(lector, start=2):
                if not any(fila.values()):  # Fila vacía
                    continue
                    
                dato_procesado = {}
                
                for campo in campos:
                    valor = fila.get(campo, '').strip()
                    
                    if campo == 'Clase' or campo == 'ID':
                        dato_procesado[campo] = valor
                    else:
                        valor_bin = mapear_a_binario(valor)
                        dato_procesado[campo] = valor_bin
                
                if es_prototipos and not dato_procesado.get('Clase'):
                    print(f"⚠️  Línea {num_linea}: Falta valor en columna 'Clase'")
                    continue
                    
                datos.append(dato_procesado)
                    
            if not datos:
                print(f"❌ ERROR: No se cargaron datos válidos de {ruta}")
                return None
                
            print(f"✅ Cargados {len(datos)} registros desde {ruta}")
            return datos
            
    except Exception as e:
        print(f"❌ ERROR leyendo {ruta}: {e}")
        return None

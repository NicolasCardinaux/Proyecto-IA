#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nnhamming.py - Red de Hamming para clasificación (Trabajo Final Integrador)

Autores: Cradinaux Nicolás, Paredez Lorenzo, Saavedra Nicolás
Fecha: Septiembre 2025
Materia: Inteligencia Artificial - UADER FCyT

Descripción:
  Lee un archivo de prototipos CSV y un archivo de casos CSV, calcula la
  distancia de Hamming entre cada caso y los prototipos, y asigna la clase
  del prototipo más cercano.

Uso:
  python Nnhamming.py prototipos.csv casos.csv
  python Nnhamming.py --help   # manual

Requisitos:
  - Archivos CSV con primera fila como header.
  - El archivo de prototipos debe contener una columna 'Clase' (case-insensitive).
  - Los valores de características deben ser binarios (0/1) o valores mapeables
    (yes/no, true/false, sí/no). El script validará y reportará errores.
  - No requiere librerías externas (solo stdlib).
"""

from __future__ import annotations
import sys
import csv
import argparse
from typing import List, Dict, Any, Optional, Tuple
import os

# ---------- Utilidad para autodetectar delimitador ----------
def detectar_delimitador(ruta_archivo: str) -> str:
    """Detecta si el archivo CSV usa ',' o ';' como delimitador."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if not first_line:
                raise ValueError("El archivo está vacío.")
            return ';' if ';' in first_line else ','
    except UnicodeDecodeError:
        raise ValueError(f"Error de codificación al leer '{ruta_archivo}'. Intenta guardarlo en UTF-8.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
    except Exception as e:
        raise RuntimeError(f"No se pudo detectar delimitador en '{ruta_archivo}': {e}")

# ---------- Parsing Args ----------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clasificador por Red de Hamming (CSV -> CSV).",
        epilog="Ejemplo: python Nnhamming.py prototipos.csv casos.csv"
    )
    parser.add_argument("prototipos", help="Ruta al CSV de prototipos (debe incluir columna 'Clase').")
    parser.add_argument("casos", help="Ruta al CSV con los casos a clasificar. Primera columna puede ser ID.")
    parser.add_argument("--id-column", default=None,
                        help="Nombre de la columna que contiene el ID del caso (por defecto: primera columna del CSV).")
    parser.add_argument("--abort-on-error", action="store_true",
                        help="Abortar inmediatamente si se encuentra un caso con error de formato.")
    parser.add_argument("--verbose", action="store_true", help="Mostrar información adicional.")
    return parser.parse_args()

# ---------- Utilidades de parsing ----------
def map_to_binary(value: str) -> Optional[int]:
    """
    Mapea un string a 0/1. Retorna None si no es mapeable.
    Acepta: '0','1','true','false','yes','no','si','sí','y','n' (case-insensitive).
    """
    if value is None:
        return None
    v = str(value).strip().lower()
    if v == '':
        return None
    trues = {'1', 'true', 'yes', 'y', 'si', 'sí', 't'}
    falses = {'0', 'false', 'no', 'n', 'f'}
    if v in trues:
        return 1
    if v in falses:
        return 0
    try:
        ival = int(v)
        if ival in (0, 1):
            return ival
    except Exception:
        return None
    return None

def cargar_prototipos(ruta_archivo: str, verbose: bool=False) -> Optional[List[Dict[str, Any]]]:
    """Carga prototipos desde CSV con validaciones robustas."""
    try:
        delim = detectar_delimitador(ruta_archivo)
        with open(ruta_archivo, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f, delimiter=delim)
            if lector.fieldnames is None:
                print(f"[ERROR] El archivo de prototipos '{ruta_archivo}' no contiene encabezado.")
                return None
            headers = [h.strip() for h in lector.fieldnames]
            if 'clase' not in [h.lower() for h in headers]:
                print(f"[ERROR] El CSV de prototipos debe incluir una columna 'Clase'. Encontrado: {headers}")
                return None

            prototipos = []
            for idx, fila in enumerate(lector, start=2):  # empieza en 2 (línea 2 real)
                if not any(fila.values()):
                    print(f"[WARN] Fila vacía en prototipos (línea {idx}), ignorada.")
                    continue
                row_norm = {k.strip(): v for k, v in fila.items()}
                clase = None
                prot = {}
                for key, raw_val in row_norm.items():
                    if key.lower() == 'clase':
                        clase = raw_val.strip()
                    else:
                        val = map_to_binary(raw_val)
                        if val is None:
                            print(f"[ERROR] Prototipo línea {idx}: valor no binario en columna '{key}': '{raw_val}'")
                            return None
                        prot[key] = val
                if not clase:
                    print(f"[ERROR] Prototipo línea {idx}: columna 'Clase' vacía.")
                    return None
                prototipos.append({'Clase': clase, **prot})

            if not prototipos:
                print("[ERROR] No se cargó ningún prototipo válido.")
                return None

            if verbose:
                print(f"[INFO] Cargados {len(prototipos)} prototipos desde '{ruta_archivo}'.")
            return prototipos

    except Exception as e:
        print(f"[ERROR] Fallo al leer prototipos: {e}")
        return None

# ---------- Distancia de Hamming ----------
def calcular_distancia_hamming(v1: Dict[str,int], v2: Dict[str,int], caracteristicas: List[str]) -> int:
    """Calcula la distancia de Hamming entre dos vectores de características."""
    return sum(1 for c in caracteristicas if v1.get(c) != v2.get(c))

# ---------- Main ----------
def main():
    args = parse_args()

    if not os.path.exists(args.prototipos):
        print(f"[ERROR] Archivo de prototipos no encontrado: {args.prototipos}")
        return 2
    if not os.path.exists(args.casos):
        print(f"[ERROR] Archivo de casos no encontrado: {args.casos}")
        return 2

    prototipos = cargar_prototipos(args.prototipos, verbose=args.verbose)
    if prototipos is None:
        return 2

    try:
        caracteristicas = [k for k in prototipos[0].keys() if k != 'Clase']
        if not caracteristicas:
            print("[ERROR] No se detectaron características en prototipos.")
            return 2
    except Exception as e:
        print(f"[ERROR] No se pudieron extraer características: {e}")
        return 2

    try:
        delim_casos = detectar_delimitador(args.casos)
        with open(args.casos, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f, delimiter=delim_casos)
            if lector.fieldnames is None:
                print(f"[ERROR] El archivo de casos '{args.casos}' no contiene encabezado.")
                return 2
            fieldnames = [h.strip() for h in lector.fieldnames]
            id_col = args.id_column if args.id_column else fieldnames[0]
            if id_col not in fieldnames:
                print(f"[ERROR] Columna ID '{id_col}' no encontrada en casos. Columnas: {fieldnames}")
                return 2

            missing = [c for c in caracteristicas if c not in fieldnames]
            if missing:
                print(f"[ERROR] Faltan columnas en '{args.casos}': {missing}")
                return 2

            print("\n--- INICIO DE CLASIFICACIÓN CON RED DE HAMMING ---")
            print(f"Prototipos: {[p['Clase'] for p in prototipos]}")
            print(f"Características: {len(caracteristicas)} -> {caracteristicas}")
            print("-" * 60)

            for lineno, fila in enumerate(lector, start=2):  # Línea 2 en adelante
                if not any(fila.values()):
                    print(f"[WARN] Fila vacía en casos (línea {lineno}), ignorada.")
                    continue
                row = {k.strip(): v for k, v in fila.items()}
                id_val = row.get(id_col, f"fila_{lineno}")
                caso_procesado = {}
                errores_en_fila = []

                for c in caracteristicas:
                    raw = row.get(c)
                    mapped = map_to_binary(raw)
                    if mapped is None:
                        errores_en_fila.append((c, raw))
                    else:
                        caso_procesado[c] = mapped

                if errores_en_fila:
                    msg = f"[ERROR] Caso '{id_val}' (línea {lineno}): valores inválidos -> " + \
                          ", ".join(f"{col}='{val}'" for col, val in errores_en_fila)
                    print(msg)
                    if args.abort_on_error:
                        return 3
                    else:
                        print(f"  > Caso '{id_val}': Clasificado como 'Indeterminado'.")
                        continue

                menor = float('inf')
                clase_asignada = "Indeterminado"
                for p in prototipos:
                    distancia = calcular_distancia_hamming(caso_procesado, p, caracteristicas)
                    if distancia < menor:
                        menor = distancia
                        clase_asignada = p['Clase']

                print(f"  > Caso '{id_val}': Clasificado como '{clase_asignada}' (Hamming={menor})")

            print("-" * 60)
            print("--- CLASIFICACIÓN FINALIZADA ---")
            return 0

    except Exception as e:
        print(f"[ERROR] Fallo procesando '{args.casos}': {e}")
        return 2

if __name__ == "__main__":
    sys.exit(main())

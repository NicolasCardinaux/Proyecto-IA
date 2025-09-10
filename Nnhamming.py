#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nnhamming.py - Red de Hamming para clasificación (Trabajo Final Integrador)

Autores: Cradinaux Nicolás, Paredez Lorenzo, Saavedra Nicolás
Fecha: Septiembre 2025
Materia: Inteligencia Artificial - UADER FCyT

Descripción:
  Implementa una red de Hamming para clasificación de patrones binarios, con una
  capa de entrada y una capa competitiva. Lee prototipos y casos desde archivos CSV,
  calcula la distancia de Hamming y asigna la clase del prototipo más cercano usando
  inhibición lateral simulada. Genera un archivo de log opcional para errores.

Uso:
  python Nnhamming.py prototipos.csv casos.csv [--id-column ID] [--metadata METADATA.csv] [--log LOG.txt] [--verbose]
  python Nnhamming.py --help   # muestra ayuda

Requisitos:
  - Python 3.6+
  - Archivos CSV con primera fila como header.
  - El archivo de prototipos debe contener una columna 'Clase' (case-insensitive).
  - Los valores de características deben ser binarios (0/1, yes/no, true/false, sí/no).
  - Opcional: archivo CSV de metadatos con columnas 'Caracteristica' y 'Tipo' (binario).
  - No requiere librerías externas (solo stdlib).

Formato de los archivos CSV:
  - prototipos.csv: Columnas 'Clase', <característica1>, <característica2>, ...
  - casos.csv: Columnas <ID>, <característica1>, <característica2>, ...
  - metadata.csv (opcional): Columnas 'Caracteristica', 'Tipo' (ejemplo: 'binario')

Instrucciones de instalación:
  1. Asegúrate de tener Python 3.6+ instalado.
  2. Guarda este script como 'Nnhamming.py'.
  3. Prepara los archivos CSV de prototipos y casos.
  4. (Opcional) Crea un archivo metadata.csv para validar características.
  5. Ejecuta: python Nnhamming.py prototipos.csv casos.csv
"""

from __future__ import annotations
import sys
import csv
import argparse
from typing import List, Dict, Any, Optional, Tuple
import os
from uuid import uuid4
import datetime

# ---------- Clase Red de Hamming ----------
class HammingNetwork:
    """Implementa una red de Hamming con capa competitiva."""
    
    def __init__(self, prototipos: List[Dict[str, Any]], caracteristicas: List[str]):
        """Inicializa la red con prototipos y características."""
        self.prototipos = prototipos
        self.caracteristicas = caracteristicas
        self.num_prototipos = len(prototipos)
        self.num_caracteristicas = len(caracteristicas)

    def calcular_distancia_hamming(self, caso: Dict[str, int], prototipo: Dict[str, int]) -> int:
        """Calcula la distancia de Hamming entre un caso y un prototipo."""
        return sum(1 for c in self.caracteristicas if caso.get(c) != prototipo.get(c))

    def clasificar(self, caso: Dict[str, int]) -> Tuple[str, int]:
        """Clasifica un caso usando distancia de Hamming e inhibición lateral simulada."""
        distancias = []
        for p in self.prototipos:
            dist = self.calcular_distancia_hamming(caso, p)
            distancias.append((dist, p['Clase']))

        # Inhibición lateral simulada: el prototipo con menor distancia "gana"
        menor_distancia = float('inf')
        clase_ganadora = "Indeterminado"
        for dist, clase in distancias:
            if dist < menor_distancia:
                menor_distancia = dist
                clase_ganadora = clase
            elif dist == menor_distancia:
                clase_ganadora = "Indeterminado"  # Empate
        return clase_ganadora, menor_distancia

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
        epilog="Ejemplo: python Nnhamming.py prototipos.csv casos.csv --metadata metadata.csv --log errores.log"
    )
    parser.add_argument("prototipos", help="Ruta al CSV de prototipos (debe incluir columna 'Clase').")
    parser.add_argument("casos", help="Ruta al CSV con los casos a clasificar. Primera columna puede ser ID.")
    parser.add_argument("--id-column", default=None,
                        help="Nombre de la columna que contiene el ID del caso (por defecto: primera columna del CSV).")
    parser.add_argument("--metadata", default=None,
                        help="Ruta al CSV de metadatos con columnas 'Caracteristica' y 'Tipo'.")
    parser.add_argument("--log", default=None,
                        help="Ruta al archivo de log para registrar errores.")
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

def cargar_metadata(ruta_metadata: str, verbose: bool = False) -> Optional[Dict[str, str]]:
    """Carga metadatos desde un archivo CSV."""
    if not ruta_metadata:
        return None
    try:
        delim = detectar_delimitador(ruta_metadata)
        with open(ruta_metadata, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f, delimiter=delim)
            if lector.fieldnames is None:
                print(f"[ERROR] El archivo de metadatos '{ruta_metadata}' no contiene encabezado.")
                return None
            if 'Caracteristica' not in lector.fieldnames or 'Tipo' not in lector.fieldnames:
                print(f"[ERROR] El CSV de metadatos debe incluir columnas 'Caracteristica' y 'Tipo'.")
                return None
            metadata = {row['Caracteristica'].strip(): row['Tipo'].strip().lower() for row in lector}
            if verbose:
                print(f"[INFO] Cargados metadatos desde '{ruta_metadata}': {metadata}")
            return metadata
    except Exception as e:
        print(f"[ERROR] Fallo al leer metadatos: {e}")
        return None

def cargar_prototipos(ruta_archivo: str, metadata: Optional[Dict[str, str]], verbose: bool = False) -> Optional[List[Dict[str, Any]]]:
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

            if metadata:
                missing = [c for c in headers if c.lower() != 'clase' and c not in metadata]
                if missing:
                    print(f"[ERROR] Columnas en prototipos no definidas en metadatos: {missing}")
                    return None

            prototipos = []
            for idx, fila in enumerate(lector, start=2):
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
                        if metadata and metadata.get(key, '').lower() != 'binario':
                            print(f"[ERROR] Prototipo línea {idx}: columna '{key}' debe ser binaria según metadatos.")
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

# ---------- Escritura de log ----------
def escribir_log(ruta_log: Optional[str], mensaje: str):
    """Escribe un mensaje en el archivo de log si se especifica."""
    if ruta_log:
        try:
            with open(ruta_log, 'a', encoding='utf-8') as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {mensaje}\n")
        except Exception as e:
            print(f"[ERROR] No se pudo escribir en el log '{ruta_log}': {e}")

# ---------- Main ----------
def main() -> int:
    args = parse_args()

    # Validar existencia de archivos
    if not os.path.exists(args.prototipos):
        print(f"[ERROR] Archivo de prototipos no encontrado: {args.prototipos}")
        escribir_log(args.log, f"Archivo de prototipos no encontrado: {args.prototipos}")
        return 2
    if not os.path.exists(args.casos):
        print(f"[ERROR] Archivo de casos no encontrado: {args.casos}")
        escribir_log(args.log, f"Archivo de casos no encontrado: {args.casos}")
        return 2
    if args.metadata and not os.path.exists(args.metadata):
        print(f"[ERROR] Archivo de metadatos no encontrado: {args.metadata}")
        escribir_log(args.log, f"Archivo de metadatos no encontrado: {args.metadata}")
        return 2

    # Cargar metadatos
    metadata = cargar_metadata(args.metadata, verbose=args.verbose)
    if args.metadata and metadata is None:
        return 2

    # Cargar prototipos
    prototipos = cargar_prototipos(args.prototipos, metadata, verbose=args.verbose)
    if prototipos is None:
        escribir_log(args.log, f"Fallo al cargar prototipos desde '{args.prototipos}'")
        return 2

    # Extraer características
    try:
        caracteristicas = [k for k in prototipos[0].keys() if k != 'Clase']
        if not caracteristicas:
            print("[ERROR] No se detectaron características en prototipos.")
            escribir_log(args.log, "No se detectaron características en prototipos")
            return 2
    except Exception as e:
        print(f"[ERROR] No se pudieron extraer características: {e}")
        escribir_log(args.log, f"No se pudieron extraer características: {e}")
        return 2

    # Inicializar red de Hamming
    red = HammingNetwork(prototipos, caracteristicas)

    try:
        delim_casos = detectar_delimitador(args.casos)
        with open(args.casos, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f, delimiter=delim_casos)
            if lector.fieldnames is None:
                print(f"[ERROR] El archivo de casos '{args.casos}' no contiene encabezado.")
                escribir_log(args.log, f"El archivo de casos '{args.casos}' no contiene encabezado")
                return 2
            fieldnames = [h.strip() for h in lector.fieldnames]
            id_col = args.id_column if args.id_column else fieldnames[0]
            if id_col not in fieldnames:
                print(f"[ERROR] Columna ID '{id_col}' no encontrada en casos. Columnas: {fieldnames}")
                escribir_log(args.log, f"Columna ID '{id_col}' no encontrada en casos")
                return 2

            missing = [c for c in caracteristicas if c not in fieldnames]
            if missing:
                print(f"[ERROR] Faltan columnas en '{args.casos}': {missing}")
                escribir_log(args.log, f"Faltan columnas en '{args.casos}': {missing}")
                return 2

            print("\n--- INICIO DE CLASIFICACIÓN CON RED DE HAMMING ---")
            print(f"Prototipos: {[p['Clase'] for p in prototipos]}")
            print(f"Características: {len(caracteristicas)} -> {caracteristicas}")
            print("-" * 60)

            for lineno, fila in enumerate(lector, start=2):
                if not any(fila.values()):
                    print(f"[WARN] Fila vacía en casos (línea {lineno}), ignorada.")
                    escribir_log(args.log, f"Fila vacía en casos (línea {lineno})")
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
                    escribir_log(args.log, msg)
                    if args.abort_on_error:
                        return 3
                    else:
                        print(f"  > Caso '{id_val}': Clasificado como 'Indeterminado'.")
                        continue

                # Clasificar usando la red
                clase_asignada, distancia = red.clasificar(caso_procesado)
                print(f"  > Caso '{id_val}': Clasificado como '{clase_asignada}' (Hamming={distancia})")
                escribir_log(args.log, f"Caso '{id_val}' clasificado como '{clase_asignada}' (Hamming={distancia})")

            print("-" * 60)
            print("--- CLASIFICACIÓN FINALIZADA ---")
            return 0

    except Exception as e:
        print(f"[ERROR] Fallo procesando '{args.casos}': {e}")
        escribir_log(args.log, f"Fallo procesando '{args.casos}': {e}")
        return 2

if __name__ == "__main__":
    sys.exit(main())
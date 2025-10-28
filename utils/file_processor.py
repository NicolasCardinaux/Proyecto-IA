import re
from patterns.regex_patterns import DELIMITERS_PATTERN

def cargar_archivo(input_file):
    """Carga el contenido de un archivo de correos"""
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{input_file}'")
        return None

def separar_correos(contenido):
    """Separa los correos individuales a partir del contenido del archivo"""
    separadores = [DELIMITERS_PATTERN]
    patron_separador = "|".join(separadores)
    correos = re.split(patron_separador, contenido)
    return [c.strip() for c in correos if c.strip()]

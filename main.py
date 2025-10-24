import sys
import os
import pandas as pd
from phishing_analyzer import PhishingAnalyzer
from utils.file_processor import cargar_archivo, separar_correos

def procesar_correos_phishing(input_file, output_file="correos_analizados.csv"):
    analyzer = PhishingAnalyzer()
    
    contenido = cargar_archivo(input_file)
    if contenido is None:
        return

    correos = separar_correos(contenido)
    if not correos:
        print("⚠️ No se encontraron correos para analizar")
        return

    resultados = []
    print("🔍 Iniciando análisis de correos...")
    
    for idx, correo in enumerate(correos, start=1):
        try:
            caracteristicas, id_correo, asunto = analyzer.analizar_correo(correo, idx)
            fila = [id_correo] + list(caracteristicas.values())
            resultados.append(fila)
            print(f"✅ {id_correo}: {asunto[:60]}...")
        except Exception as e:
            print(f"❌ Error analizando correo {idx}: {e}")
            continue

    if resultados:
        columnas = [
            "ID", "AsuntoUrgente", "SolicitaCredenciales", "EnlacesSospechosos",
            "DominioRemitenteSospechoso", "ErroresOrtograficos", "FaltaInformacionContacto",
            "AmenazasConsecuencias", "PremioInexperado", "ActualizacionUrgente", "SaludoGenerico"
        ]
        df = pd.DataFrame(resultados, columns=columnas)
        df.to_csv(output_file, index=False, encoding="utf-8")
        print(f"\n✅ Análisis completado! Resultados guardados en: {os.path.abspath(output_file)}")
    else:
        print("❌ No se pudieron analizar correos")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_correos.txt> [archivo_salida.csv]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "correos_analizados.csv"
        if not os.path.exists(input_file):
            print(f"❌ Error: El archivo '{input_file}' no existe")
        else:
            procesar_correos_phishing(input_file, output_file)
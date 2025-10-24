"""
Nnhamming.py - Red de Hamming para Detección de Phishing
Trabajo Final Integrador - Inteligencia Artificial - UADER FCyT

Autores: Cardinaux Nicolás, Paredes Lorenzo, Saavedra Nicolás
Fecha: Septiembre 2025

Descripción:
    Implementa una red de Hamming optimizada para clasificación de correos
    electrónicos como Legítimos o Phishing basado en características binarias.
"""

import sys
import csv
import argparse
import os
from typing import List, Dict, Any, Tuple
from collections import Counter
from utils.utils import cargar_datos_csv

class RedHamming:
    """Implementa una red de Hamming para clasificación binaria."""

    def __init__(self, prototipos: List[Dict[str, Any]]):
        """
        Inicializa la red con prototipos de entrenamiento.
        """
        self.prototipos = prototipos
        # Extraer características comunes entre todos los prototipos
        self.caracteristicas = self._extraer_caracteristicas_comunes()
        self.num_prototipos = len(prototipos)
        self.num_caracteristicas = len(self.caracteristicas)

        print(f"🔧 Características para clasificación: {self.caracteristicas}")

    def _extraer_caracteristicas_comunes(self):
        """Extrae características comunes excluyendo 'Clase' e 'ID'"""
        if not self.prototipos:
            return []

        # Tomar características del primer prototipo excluyendo 'Clase' e 'ID'
        caracteristicas = [k for k in self.prototipos[0].keys() 
                          if k not in ['Clase', 'ID'] and self.prototipos[0][k] is not None]
        return caracteristicas

    def calcular_distancia_hamming(self, caso: Dict[str, int], prototipo: Dict[str, int]) -> int:
        """
        Calcula la distancia de Hamming entre un caso y un prototipo.
        """
        distancia = 0
        for caracteristica in self.caracteristicas:
            valor_caso = caso.get(caracteristica)
            valor_prototipo = prototipo.get(caracteristica)

            # Si alguno es None, contar como diferencia
            if valor_caso is None or valor_prototipo is None:
                distancia += 1
            elif valor_caso != valor_prototipo:
                distancia += 1
        return distancia

    def clasificar(self, caso: Dict[str, int]) -> Tuple[str, int]:
        """
        Clasifica un caso usando la red de Hamming.
        """
        # Filtrar solo las características que tenemos en el caso
        caso_filtrado = {
            k: v for k, v in caso.items() if k in self.caracteristicas and v is not None
            }

        if not caso_filtrado:
            return "Indeterminado", -1

        # Calcular distancias a todos los prototipos
        distancias = []
        for prototipo in self.prototipos:
            dist = self.calcular_distancia_hamming(caso_filtrado, prototipo)
            distancias.append((dist, prototipo['Clase']))

        # Encontrar la menor distancia
        menor_distancia = min(dist for dist, _ in distancias)

        # Contar votos entre los prototipos con menor distancia
        votos = Counter(clase for dist, clase in distancias if dist == menor_distancia)

        # Desempatar por proximidad adicional si hay empate
        if len(votos) > 1:
            # En caso de empate, usar el primer prototipo más cercano
            clase_ganadora = distancias[0][1]
        else:
            clase_ganadora = votos.most_common(1)[0][0] if votos else "Indeterminado"

        return clase_ganadora, menor_distancia

def main():
    """Función principal del programa."""
    parser = argparse.ArgumentParser(
        description='Red de Hamming para Detección de Phishing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
Ejemplos de uso:
  python {sys.argv[0]} prototipos.csv casos.csv
  python {sys.argv[0]} prototipos.csv casos.csv --verbose

Características:
  • Clasificación robusta de correos como Legítimo/Phishing
  • Manejo flexible de características
  • Soporte para diferentes formatos CSV
        '''
    )

    parser.add_argument('prototipos', help='Archivo CSV con prototipos de entrenamiento')
    parser.add_argument('casos', help='Archivo CSV con casos a clasificar')
    parser.add_argument('--verbose', action='store_true', 
                       help='Mostrar información detallada')
    parser.add_argument('--salida', default='resultados_clasificacion.csv',
                       help='Archivo de salida para resultados')

    args = parser.parse_args()

    print("🚀 INICIANDO SISTEMA DE DETECCIÓN DE PHISHING")
    print("=" * 60)

    # Validar archivos de entrada
    for archivo in [args.prototipos, args.casos]:
        if not os.path.exists(archivo):
            print(f"❌ ERROR: Archivo no encontrado: {archivo}")
            return 1

    # Cargar prototipos
    print("📥 Cargando prototipos de entrenamiento...")
    prototipos = cargar_datos_csv(args.prototipos, es_prototipos=True)
    if not prototipos:
        return 1

    # Cargar casos a clasificar
    print("📥 Cargando casos para clasificación...")
    casos = cargar_datos_csv(args.casos, es_prototipos=False)
    if not casos:
        return 1

    print(f"📨 Casos a clasificar: {len(casos)}")

    # Inicializar red
    try:
        red = RedHamming(prototipos)
    except Exception as e:
        print(f"❌ ERROR inicializando red: {e}")
        return 1

    # Procesar clasificación
    print("\n🔍 INICIANDO CLASIFICACIÓN...")
    print("-" * 60)

    resultados = []
    estadisticas = Counter()

    for caso in casos:
        try:
            id_caso = caso.get('ID', 'Desconocido')

            # Clasificar
            clase_predicha, distancia = red.clasificar(caso)

            # Actualizar estadísticas
            estadisticas[clase_predicha] += 1

            # Guardar resultado
            resultados.append({
                'ID': id_caso,
                'Clase_Predicha': clase_predicha,
                'Distancia_Hamming': distancia
            })

            if args.verbose:
                print(f"✅ {id_caso} -> {clase_predicha} (distancia: {distancia})")

        except Exception as e:
            print(f"❌ ERROR clasificando caso {id_caso}: {e}")
            estadisticas['Error'] += 1
            resultados.append({
                'ID': id_caso,
                'Clase_Predicha': 'Error',
                'Distancia_Hamming': -1,
                'Error': str(e)
            })

    # Generar reporte final
    print("\n📊 REPORTE FINAL DE CLASIFICACIÓN")
    print("=" * 60)

    total = len(casos)
    for clase, count in estadisticas.items():
        porcentaje = (count / total) * 100
        print(f"   {clase:<12}: {count:>3} casos ({porcentaje:5.1f}%)")

    # Guardar resultados en CSV
    try:
        with open(args.salida, 'w', newline='', encoding='utf-8') as f:
            if resultados:
                campos = resultados[0].keys()
                escritor = csv.DictWriter(f, fieldnames=campos, delimiter=';')
                escritor.writeheader()
                escritor.writerows(resultados)

        print(f"💾 Resultados guardados en: {args.salida}")
    except Exception as e:
        print(f"❌ ERROR guardando resultados: {e}")

    print("\n✅ PROCESO COMPLETADO EXITOSAMENTE")
    return 0

if __name__ == '__main__':
    sys.exit(main())

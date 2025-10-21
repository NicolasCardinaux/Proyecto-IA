import re
import pandas as pd
import sys
import os
from urllib.parse import urlparse
import tldextract
from collections import Counter

class PhishingAnalyzer:
    def __init__(self):
        # Patrones específicos para phishing
        self.URGENTE_KEYWORDS = [
            'urgente', 'inmediato', 'acción requerida', 'cuenta suspendida', 'bloqueada',
            'problema de seguridad', 'verificación necesaria', 'actuar ahora', 'última oportunidad',
            'alerta de seguridad', 'expira pronto', 'confirmar ahora', 'validar cuenta',
            'importante', 'atención', 'critical', 'action required', 'immediately'
        ]
        
        self.CREDENCIALES_KEYWORDS = [
            'contraseña', 'password', 'credenciales', 'iniciar sesión', 'login',
            'verificar cuenta', 'confirmar identidad', 'datos de acceso',
            'actualizar información', 'seguridad de la cuenta', 'clave', 'usuario',
            'credential', 'account verification', 'security update'
        ]
        
        self.AMENAZAS_KEYWORDS = [
            'permanente', 'perderá acceso', 'eliminaremos', 'suspenderemos',
            'bloqueo permanente', 'consecuencias', 'acción legal', 'multa',
            'tarifas adicionales', 'cobro automático', 'suspend', 'terminate',
            'close your account', 'permanent loss'
        ]
        
        self.PREMIO_KEYWORDS = [
            'ganador', 'premio', 'sorteo', 'felicitaciones', 'has sido seleccionado',
            'reclama tu premio', 'regalo especial', 'oferta exclusiva', 'ganaste',
            'winner', 'congratulations', 'selected', 'prize', 'reward'
        ]
        
        self.ACTUALIZACION_KEYWORDS = [
            'actualizar', 'verificar', 'confirmar', 'validar', 'completar',
            'renovar información', 'revisar cuenta', 'mejorar seguridad',
            'update', 'verify', 'confirm', 'validate', 'renew'
        ]
        
        # Acortadores de URL
        self.URL_SHORTENERS = {
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd',
            'buff.ly', 'shorte.st', 'adf.ly', 'tiny.cc', 'bitly.com',
            'rebrand.ly', 'cutt.ly', 'shorturl.at'
        }
        
        # Dominios genéricos comunes
        self.DOMINIOS_GENERICOS = {
            'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'live.com',
            'aol.com', 'icloud.com', 'protonmail.com', 'yandex.com'
        }
        
        # Expresiones regulares compiladas
        self.REGEX = {
            "errores": re.compile(r'\b(urjente|nesesita|actualisar|verificacion|hasido|disculpa|grasias|kiero|q|tmb|diculpa|vienbenido|nesesitas|porfavor|ud\.?)\b', re.I),
            "enlaces": re.compile(r'https?://[^\s/$.?#].[^\s]*', re.I),
            "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            "saludo_generico": re.compile(r'^(estimado cliente|querido usuario|apreciado cliente|dear customer|hola,|hi there|greetings|premium user|valued customer)', re.I | re.M),
            "telefono": re.compile(r'(\+\d{1,3}[-.]?)?\d{2,4}[-.]?\d{3,4}[-.]?\d{3,4}'),
        }

    def generar_id_correo(self, numero_correo):
        """Genera ID simple: Correo01, Correo02, etc."""
        return f"Correo{numero_correo:02d}"

    def analizar_asunto(self, asunto):
        """Analiza el asunto en busca de indicadores de phishing"""
        if not asunto:
            return 0
            
        asunto_lower = asunto.lower()
        
        # Verificar palabras urgentes
        urgente = any(keyword in asunto_lower for keyword in self.URGENTE_KEYWORDS)
        
        # Verificar exceso de mayúsculas
        letras = [c for c in asunto if c.isalpha()]
        if letras:
            mayusculas = sum(1 for c in letras if c.isupper())
            ratio_mayusculas = mayusculas / len(letras)
            formato_sospechoso = ratio_mayusculas > 0.6
        else:
            formato_sospechoso = False
            
        # Verificar símbolos excesivos
        simbolos_excesivos = len(re.findall(r'[!¡?¿]{2,}', asunto)) > 0
        
        return 1 if urgente or formato_sospechoso or simbolos_excesivos else 0

    def analizar_solicitud_credenciales(self, cuerpo):
        """Busca solicitudes de información sensible"""
        if not cuerpo:
            return 0
            
        cuerpo_lower = cuerpo.lower()
        
        # Verificar palabras clave de credenciales
        tiene_keywords = any(keyword in cuerpo_lower for keyword in self.CREDENCIALES_KEYWORDS)
        
        # Verificar patrones de formularios
        patrones_formulario = re.findall(r'(ingrese|introduzca|complete|rellene|proporcione).*?(contraseña|password|usuario|credencial|tarjeta|cuenta|dni)', cuerpo_lower)
        
        return 1 if tiene_keywords or patrones_formulario else 0

    def analizar_enlaces(self, cuerpo, remitente_dominio):
        """Analiza enlaces en busca de phishing"""
        enlaces = self.REGEX["enlaces"].findall(cuerpo)
        if not enlaces:
            return 0, 0
            
        usa_acortador = 0
        dominio_sospechoso = 0
        
        for enlace in enlaces:
            try:
                parsed = urlparse(enlace)
                dominio_enlace = parsed.netloc.lower()
                
                # Verificar acortadores
                if any(short in dominio_enlace for short in self.URL_SHORTENERS):
                    usa_acortador = 1
                    continue
                
                # Extraer dominio base para comparación
                ext = tldextract.extract(dominio_enlace)
                dominio_base_enlace = f"{ext.domain}.{ext.suffix}"
                
                # Verificar si el dominio del remitente es diferente al del enlace
                if remitente_dominio:
                    ext_remitente = tldextract.extract(remitente_dominio)
                    dominio_base_remitente = f"{ext_remitente.domain}.{ext_remitente.suffix}"
                    
                    if dominio_base_remitente != dominio_base_enlace:
                        dominio_sospechoso = 1
                                
            except Exception:
                continue
                
        return usa_acortador, dominio_sospechoso

    def analizar_remitente(self, remitente_email, remitente_nombre):
        """Analiza el remitente en busca de suplantación"""
        if not remitente_email:
            return 1
            
        try:
            if '@' not in remitente_email:
                return 1
                
            dominio = remitente_email.split('@')[1].lower()
            
            # Verificar si usa dominio genérico
            if dominio in self.DOMINIOS_GENERICOS:
                return 1
                        
            # Verificar formato sospechoso del dominio
            if re.search(r'\d{4,}|\-{2,}|_{2,}', dominio):
                return 1
                
        except Exception:
            return 1
            
        return 0

    def analizar_errores(self, cuerpo):
        """Busca errores ortográficos y gramaticales típicos de phishing"""
        if not cuerpo:
            return 0
            
        # Buscar errores comunes
        if self.REGEX["errores"].search(cuerpo):
            return 1
            
        # Buscar repetición excesiva de signos
        if len(re.findall(r'[!¡]{3,}', cuerpo)) > 0:
            return 1
            
        return 0

    def analizar_falta_contacto(self, cuerpo):
        """Verifica falta de información de contacto legítima"""
        if not cuerpo:
            return 1
            
        # Buscar información de contacto legítima
        tiene_telefono = self.REGEX["telefono"].search(cuerpo)
        tiene_direccion = re.search(r'(calle|avenida|av\.|número|nro|piso|departamento|depto|address|street|ave)', cuerpo, re.I)
        tiene_empresa = re.search(r'(inc\.|llc|s\.a\.|corporation|company|corp|ltda)', cuerpo, re.I)
        
        return 0 if (tiene_telefono or tiene_direccion or tiene_empresa) else 1

    def analizar_amenazas(self, cuerpo):
        """Busca lenguaje amenazante o de consecuencias"""
        if not cuerpo:
            return 0
            
        cuerpo_lower = cuerpo.lower()
        return 1 if any(keyword in cuerpo_lower for keyword in self.AMENAZAS_KEYWORDS) else 0

    def analizar_premio(self, cuerpo):
        """Busca anuncios de premios inesperados"""
        if not cuerpo:
            return 0
            
        cuerpo_lower = cuerpo.lower()
        return 1 if any(keyword in cuerpo_lower for keyword in self.PREMIO_KEYWORDS) else 0

    def analizar_actualizacion(self, cuerpo):
        """Busca solicitudes de actualización urgente"""
        if not cuerpo:
            return 0
            
        cuerpo_lower = cuerpo.lower()
        return 1 if any(keyword in cuerpo_lower for keyword in self.ACTUALIZACION_KEYWORDS) else 0

    def analizar_saludo(self, cuerpo):
        """Busca saludos genéricos"""
        if not cuerpo:
            return 1
            
        return 1 if self.REGEX["saludo_generico"].search(cuerpo) else 0

    def analizar_correo(self, correo_completo, numero_correo):
        """Analiza un correo completo y extrae características"""
        try:
            lines = correo_completo.split('\n')
            remitente = ""
            asunto = ""
            cuerpo_lines = []
            
            in_headers = True
            for line in lines:
                line_lower = line.lower()
                if in_headers:
                    if line_lower.startswith('from:'):
                        remitente = line[5:].strip()
                    elif line_lower.startswith('subject:'):
                        asunto = line[8:].strip()
                    elif line.strip() == '':
                        in_headers = False
                else:
                    cuerpo_lines.append(line)
                    
            cuerpo = '\n'.join(cuerpo_lines)
            
            # Extraer información del remitente
            remitente_email = ""
            remitente_nombre = "Desconocido"
            
            if remitente:
                if '<' in remitente and '>' in remitente:
                    match = re.search(r'(.*?)<(.*?)>', remitente)
                    if match:
                        remitente_nombre = match.group(1).strip().strip('"')
                        remitente_email = match.group(2).strip()
                else:
                    remitente_email = remitente
                    # Intentar extraer nombre si está entre comillas
                    match = re.search(r'"([^"]*)"', remitente)
                    if match:
                        remitente_nombre = match.group(1).strip()
            
            remitente_dominio = ""
            if '@' in remitente_email:
                remitente_dominio = remitente_email.split('@')[1].lower()
            
            # Generar ID simple
            id_correo = self.generar_id_correo(numero_correo)
            
            # Realizar análisis de características
            caracteristicas = {}
            
            caracteristicas["AsuntoUrgente"] = self.analizar_asunto(asunto)
            caracteristicas["SolicitaCredenciales"] = self.analizar_solicitud_credenciales(cuerpo)
            
            usa_acortador, dominio_sospechoso = self.analizar_enlaces(cuerpo, remitente_dominio)
            caracteristicas["EnlacesSospechosos"] = 1 if (usa_acortador or dominio_sospechoso) else 0
            
            caracteristicas["DominioRemitenteSospechoso"] = self.analizar_remitente(remitente_email, remitente_nombre)
            caracteristicas["ErroresOrtograficos"] = self.analizar_errores(cuerpo)
            caracteristicas["FaltaInformacionContacto"] = self.analizar_falta_contacto(cuerpo)
            caracteristicas["AmenazasConsecuencias"] = self.analizar_amenazas(cuerpo)
            caracteristicas["PremioInexperado"] = self.analizar_premio(cuerpo)
            caracteristicas["ActualizacionUrgente"] = self.analizar_actualizacion(cuerpo)
            caracteristicas["SaludoGenerico"] = self.analizar_saludo(cuerpo)
            
            return caracteristicas, id_correo, asunto
            
        except Exception as e:
            # En caso de error, retornar valores por defecto
            caracteristicas = {
                "AsuntoUrgente": 0, "SolicitaCredenciales": 0, "EnlacesSospechosos": 0,
                "DominioRemitenteSospechoso": 1, "ErroresOrtograficos": 0, "FaltaInformacionContacto": 1,
                "AmenazasConsecuencias": 0, "PremioInexperado": 0, "ActualizacionUrgente": 0, "SaludoGenerico": 1
            }
            return caracteristicas, f"Correo{numero_correo:02d}", "Error en análisis"

def procesar_correos_phishing(input_file, output_file="correos_analizados.csv"):
    """
    Procesa un archivo de texto con correos y genera un CSV con características de phishing
    """
    analyzer = PhishingAnalyzer()
    
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{input_file}'")
        return

    # Separar correos individuales
    separadores = [r"\nFrom:", r"\nDe:", r"\nRecibidos\n", r"\nReceived:"]
    patron_separador = "|".join(separadores)
    correos = re.split(patron_separador, contenido)
    correos = [c.strip() for c in correos if c.strip()]

    if not correos:
        print("⚠️ No se encontraron correos para analizar")
        return

    resultados = []
    
    print("🔍 Iniciando análisis de correos...")
    for idx, correo in enumerate(correos, start=1):
        try:
            caracteristicas, id_correo, asunto = analyzer.analizar_correo(correo, idx)
            
            # Agregar a resultados
            fila = [id_correo] + list(caracteristicas.values())
            resultados.append(fila)
            
            print(f"✅ {id_correo}: {asunto[:60]}...")
            
        except Exception as e:
            print(f"❌ Error analizando correo {idx}: {e}")
            continue

    # Columnas para el CSV
    columnas = [
        "ID", "AsuntoUrgente", "SolicitaCredenciales", "EnlacesSospechosos",
        "DominioRemitenteSospechoso", "ErroresOrtograficos", "FaltaInformacionContacto",
        "AmenazasConsecuencias", "PremioInexperado", "ActualizacionUrgente", "SaludoGenerico"
    ]

    # Crear DataFrame y guardar
    if resultados:
        df = pd.DataFrame(resultados, columns=columnas)
        df.to_csv(output_file, index=False, encoding="utf-8")
        
        print(f"\n✅ Análisis completado!")
        print(f"📁 Resultados guardados en: {os.path.abspath(output_file)}")
        print(f"📊 Total de correos analizados: {len(resultados)}")
        
        # Mostrar resumen estadístico
        print("\n📈 Resumen de características detectadas:")
        for col in columnas[1:]:
            count = df[col].sum()
            porcentaje = (count / len(resultados)) * 100
            print(f"   {col}: {count}/{len(resultados)} ({porcentaje:.1f}%)")
    else:
        print("❌ No se pudieron analizar correos")

if __name__ == "__main__":
    print("🛡️  Analizador de Phishing - Detección de Correos Fraudulentos")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUso: python procesar_correos.py <archivo_correos.txt> [archivo_salida.csv]")
        print("\nEjemplos:")
        print("  python procesar_correos.py correos.txt")
        print("  python procesar_correos.py correos.txt resultado.csv")
        print("\nEl archivo de correos debe tener formato:")
        print("  From: \"Nombre\" <email@dominio.com>")
        print("  Subject: Asunto del correo")
        print("  ...cuerpo del correo...")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "correos_analizados.csv"
        
        if not os.path.exists(input_file):
            print(f"❌ Error: El archivo '{input_file}' no existe")
        else:
            procesar_correos_phishing(input_file, output_file)
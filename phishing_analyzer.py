import re
from urllib.parse import urlparse
import tldextract
from patterns.keywords import URGENTE_KEYWORDS, CREDENCIALES_KEYWORDS, AMENAZAS_KEYWORDS, PREMIO_KEYWORDS, ACTUALIZACION_KEYWORDS, URL_SHORTENERS, DOMINIOS_GENERICOS
from patterns.regex_patterns import ERRORS_PATTERN, LINKS_PATTERN, EMAIL_PATTERN, GREETINGS_PATTERN, PHONE_PATTERN


class PhishingAnalyzer:
    def __init__(self):
        # Patrones específicos para phishing
        self.URGENTE_KEYWORDS = URGENTE_KEYWORDS
        self.CREDENCIALES_KEYWORDS = CREDENCIALES_KEYWORDS
        self.AMENAZAS_KEYWORDS = AMENAZAS_KEYWORDS
        self.PREMIO_KEYWORDS = PREMIO_KEYWORDS
        self.ACTUALIZACION_KEYWORDS = ACTUALIZACION_KEYWORDS
        self.URL_SHORTENERS = URL_SHORTENERS
        self.DOMINIOS_GENERICOS = DOMINIOS_GENERICOS

        # Expresiones regulares compiladas
        self.REGEX = {
            "errores": re.compile(ERRORS_PATTERN, re.I),
            "enlaces": re.compile(LINKS_PATTERN, re.I),
            "email": re.compile(EMAIL_PATTERN),
            "saludo_generico": re.compile(GREETINGS_PATTERN, re.I | re.M),
            "telefono": re.compile(PHONE_PATTERN)
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
        urgente = any(
            keyword in asunto_lower for keyword in self.URGENTE_KEYWORDS)

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
        tiene_keywords = any(
            keyword in cuerpo_lower for keyword in self.CREDENCIALES_KEYWORDS)

        # Verificar patrones de formularios
        patrones_formulario = re.findall(
            r'(ingrese|introduzca|complete|rellene|proporcione).*?(contraseña|password|usuario|credencial|tarjeta|cuenta|dni)', cuerpo_lower)

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

    def analizar_remitente(self, remitente_email):
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
        tiene_direccion = re.search(
            r'(calle|avenida|av\.|número|nro|piso|departamento|depto|address|street|ave)', cuerpo, re.I)
        tiene_empresa = re.search(
            r'(inc\.|llc|s\.a\.|corporation|company|corp|ltda)', cuerpo, re.I)

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

            if remitente:
                if '<' in remitente and '>' in remitente:
                    match = re.search(r'(.*?)<(.*?)>', remitente)
                    if match:
                        remitente_email = match.group(2).strip()
                else:
                    remitente_email = remitente
                    # Intentar extraer nombre si está entre comillas
                    match = re.search(r'"([^"]*)"', remitente)

            remitente_dominio = ""
            if '@' in remitente_email:
                remitente_dominio = remitente_email.split('@')[1].lower()

            # Generar ID simple
            id_correo = self.generar_id_correo(numero_correo)

            # Realizar análisis de características
            caracteristicas = {}

            caracteristicas["AsuntoUrgente"] = self.analizar_asunto(asunto)
            caracteristicas["SolicitaCredenciales"] = self.analizar_solicitud_credenciales(
                cuerpo)

            usa_acortador, dominio_sospechoso = self.analizar_enlaces(
                cuerpo, remitente_dominio)
            caracteristicas["EnlacesSospechosos"] = 1 if (
                usa_acortador or dominio_sospechoso) else 0

            caracteristicas["DominioRemitenteSospechoso"] = self.analizar_remitente(
                remitente_email)
            caracteristicas["ErroresOrtograficos"] = self.analizar_errores(
                cuerpo)
            caracteristicas["FaltaInformacionContacto"] = self.analizar_falta_contacto(
                cuerpo)
            caracteristicas["AmenazasConsecuencias"] = self.analizar_amenazas(
                cuerpo)
            caracteristicas["PremioInexperado"] = self.analizar_premio(cuerpo)
            caracteristicas["ActualizacionUrgente"] = self.analizar_actualizacion(
                cuerpo)
            caracteristicas["SaludoGenerico"] = self.analizar_saludo(cuerpo)

            return caracteristicas, id_correo, asunto

        except Exception:
            # En caso de error, retornar valores por defecto
            caracteristicas = {
                "AsuntoUrgente": 0, "SolicitaCredenciales": 0, "EnlacesSospechosos": 0,
                "DominioRemitenteSospechoso": 1, "ErroresOrtograficos": 0,
                "FaltaInformacionContacto": 1, "AmenazasConsecuencias": 0,
                "PremioInexperado": 0, "ActualizacionUrgente": 0, "SaludoGenerico": 1
            }
            return caracteristicas, f"Correo{numero_correo:02d}", "Error en análisis"

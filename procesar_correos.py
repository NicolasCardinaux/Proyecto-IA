import re
import pandas as pd
import sys
import os
from urllib.parse import urlparse

# --- LISTAS DE PALABRAS CLAVE Y PATRONES (VERSIÓN EXTENDIDA) ---

# Palabras clave y patrones para cada criterio
OFERTA_KEYWORDS = [
    'oferta', 'gratis', 'premio', 'regalo', 'cupón', 'voucher', 'desbloquea',
    'free shipping', 'envío gratis', 'sample', 'prueba gratis', 'gana', 'win',
    'sorteo', 'rifa', 'lotería', 'giveaway', 'concurso', 'freebie', 'muestra',
    'bono', 'cashback', 'recompensa', 'claim your', 'canjear', 'acceso gratuito',
    'sin costo', 'de regalo', 'por nuestra cuenta', 'bogo', '2x1', 'compre uno'
]
PROMO_KEYWORDS = [
    'descuento', 'rebaja', 'exclusivo', 'especial', 'promoción', 'promocion',
    'ahorra', 'ahorro', 'imperdible', 'único', 'only today', 'deal', 'sale',
    'super oferta', 'clearance', 'liquidación', 'limited time', 'por tiempo limitado',
    'black friday', 'cyber monday', 'revolucionario', 'secreto', 'invitación especial',
    'acceso anticipado', 'best seller', 'increíble', 'asombroso', 'garantizado'
]
PERSONAL_INFO_KEYWORDS = [
    'contraseña', 'password', 'datos bancarios', 'tarjeta de crédito', 'credit card',
    'número de cuenta', 'iban', 'cuil', 'cuit', 'cult', 'dni', 'documento', 'ssn',
    'pin', 'clave', 'security code', 'número de seguro social', 'fecha de nacimiento',
    'actualiza tus datos', 'verifica tu cuenta', 'información financiera',
    'confirmar tus credenciales', 'actualizar información de pago', 'billing information'
]
CTA_KEYWORDS = [
    'clic aquí', 'click here', 'visite', 'descubra', 'ingrese', 'entra ya', 'registrate',
    'create account', 'compra', 'shop now', 'comprar ahora', 'usar cupón', 'aprovecha',
    'claim', 'get started', 'ver más', 'leer más', 'learn more', 'descargar ahora'
]
URGENTE_KEYWORDS = [
    'actúe ahora', 'expira pronto', 'última oportunidad', 'no te lo pierdas',
    'hurry', 'last chance', 'final hours', 'termina hoy', 'solo por hoy', 'solo hoy',
    'apúrate', 'urgente', 'oferta termina', 'stock limitado', 'no esperes', 'act now',
    'antes de que se acabe', 'countdown'
]
SOSPECHOSOS_DOMAINS_KEYWORDS = ['secure', 'login', 'account', 'verify', 'support', 'service', 'online', 'bank', 'info']
URL_SHORTENERS = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd']

# --- EXPRESIONES REGULARES ---
REGEX = {
    "errores": re.compile(r'\b(kiero|xq|q|tmb|diculpa|grasias|vienbenido|nesesitas|porfavor|ud\.?)\b|(\w)\1{2,}| \S*@\S* ', re.I),
    "emoticonos": re.compile(r'[😊💡💜😀😍😉🤔🔥🎉💰📱🚀⭐✨⚡️💸🤑📈💯❗️‼️🚨🎁🛒]'),
    "saludo_generico": re.compile(r'^(estimado cliente|querido usuario|apreciado cliente|dear customer|hola,|hi there|greetings)', re.I | re.M),
    "promo_patterns": re.compile(r'(\b\d+\s*%\s*(off|dto\.|descuento)\b)', re.I),
    "urgente_patterns": re.compile(r'(\bexpira en\b|\bsolo quedan\b|\búltimas horas\b|\btermina a medianoche\b|\bsolo por \d+ horas\b)', re.I),
    "link_extractor": re.compile(r'https?://[^\s/$.?#].[^\s]*', re.I)
}

# --- FUNCIONES DE ANÁLISIS AUXILIARES ---

def check_subject_case(subject):
    """Verifica si hay un uso excesivo de mayúsculas o símbolos en el asunto."""
    if not subject or len(subject) < 5:
        return 0
    alpha_chars = [c for c in subject if c.isalpha()]
    if not alpha_chars:
        return 1 # El asunto solo contiene símbolos
    upper_ratio = sum(1 for c in alpha_chars if c.isupper()) / len(alpha_chars)
    return 1 if upper_ratio > 0.7 or re.search(r'[!¡?¿]{2,}', subject) else 0

def check_keywords(text, keywords):
    """Función genérica para verificar la presencia de palabras clave."""
    return 1 if any(word in text for word in keywords) else 0

def check_multiple_ctas(text, keywords):
    """Cuenta cuántas frases CTA *diferentes* están presentes."""
    found_ctas = {word for word in keywords if word in text}
    return 1 if len(found_ctas) > 2 else 0

def check_suspicious_sender(sender_email, sender_name):
    """Analiza el remitente en busca de signos de suplantación de identidad."""
    if not sender_email:
        return 0
    try:
        domain = sender_email.split('@')[1]
        # Comprueba si el dominio contiene palabras sospechosas
        if any(keyword in domain for keyword in SOSPECHOSOS_DOMAINS_KEYWORDS):
            # Comprueba si el nombre pretende ser una marca conocida pero el dominio no coincide
            for brand in ['google', 'microsoft', 'paypal', 'amazon', 'apple', 'netflix']:
                if brand in sender_name.lower() and brand not in domain:
                    return 1
    except IndexError:
        return 0 # Formato de correo electrónico no válido
    return 0
    
def check_links(text):
    """Analiza todos los enlaces en el texto en busca de acortadores y cantidad excesiva."""
    links = REGEX["link_extractor"].findall(text)
    if not links:
        return 0, 0
    
    uses_shortener = 0
    for link in links:
        try:
            domain = urlparse(link).netloc.lower().replace('www.', '')
            if any(shortener in domain for shortener in URL_SHORTENERS):
                uses_shortener = 1
                break
        except Exception:
            continue

    # Heurística: más de 1 enlace por cada 10 palabras es excesivo
    word_count = len(text.split())
    excessive_links = 1 if word_count > 0 and (len(links) / word_count) > 0.1 else 0

    return uses_shortener, excessive_links

# --- FUNCIÓN PRINCIPAL DE PROCESAMIENTO ---

def analizar_correos(input_file, output_file="correos_analizados.csv"):
    """
    Analiza un archivo de texto de correos, extrae un conjunto extendido de características
    y genera un CSV con indicadores binarios (0 o 1) para cada una.
    """
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{input_file}' no fue encontrado.")
        return

    correos = re.split(r"\nRecibidos\n", text)
    correos = [c.strip() for c in correos if c.strip()]

    if not correos:
        print("⚠️ No se encontraron correos para analizar.")
        return

    resultados = []

    for idx, correo in enumerate(correos, start=1):
        correo_lower = correo.lower()

        # --- Extracción de Datos ---
        remitente_match = re.search(r"^(.*?) <(.*?)>", correo, re.M)
        remitente_name = remitente_match.group(1).strip() if remitente_match else "Desconocido"
        remitente_email = remitente_match.group(2).strip() if remitente_match else ""
        
        asunto_match = re.search(r"^(.*?)\n", correo)
        asunto = asunto_match.group(1).strip() if asunto_match else ""

        # --- Detección de Características ---
        features = {}
        features["AsuntoEnMayusculas"] = check_subject_case(asunto)
        features["ContieneOferta"] = check_keywords(correo_lower, OFERTA_KEYWORDS)
        features["UsaLenguajePromocional"] = 1 if features["ContieneOferta"] or REGEX["promo_patterns"].search(correo_lower) or check_keywords(correo_lower, PROMO_KEYWORDS) else 0
        features["TieneErroresOrtograficos"] = 1 if REGEX["errores"].search(correo) else 0
        features["SolicitaInfoPersonal"] = check_keywords(correo_lower, PERSONAL_INFO_KEYWORDS)
        features["ContieneMultiplesLlamadasAccion"] = check_multiple_ctas(correo_lower, CTA_KEYWORDS)
        features["EsUrgente"] = 1 if REGEX["urgente_patterns"].search(correo_lower) or check_keywords(correo_lower, URGENTE_KEYWORDS) else 0
        features["UsaEmoticonos"] = 1 if REGEX["emoticonos"].search(correo) else 0
        features["EsRespuesta"] = 1 if asunto.upper().startswith(("RE:", "AW:", "RV:", "FWD:")) else 0
        features["SaludoGenerico"] = 1 if REGEX["saludo_generico"].search(correo) else 0
        
        # Características Avanzadas
        features["RemitenteSospechoso"] = check_suspicious_sender(remitente_email, remitente_name)
        uses_shortener, excessive_links = check_links(correo)
        features["UsaAcortadorURL"] = uses_shortener
        features["ExcesoDeEnlaces"] = excessive_links

        id_correo = f"{idx:02d}/{remitente_name}"
        
        resultados.append([
            id_correo, features["AsuntoEnMayusculas"], features["ContieneOferta"], features["UsaLenguajePromocional"],
            features["TieneErroresOrtograficos"], features["SolicitaInfoPersonal"], features["ContieneMultiplesLlamadasAccion"],
            features["EsUrgente"], features["UsaEmoticonos"], features["EsRespuesta"], features["SaludoGenerico"],
            features["RemitenteSospechoso"], features["UsaAcortadorURL"], features["ExcesoDeEnlaces"]
        ])

    # --- Generación del CSV ---
    columns = [
        "ID", "AsuntoEnMayusculas", "ContieneOferta", "UsaLenguajePromocional",
        "TieneErroresOrtograficos", "SolicitaInfoPersonal",
        "ContieneMultiplesLlamadasAccion", "EsUrgente", "UsaEmoticonos",
        "EsRespuesta", "SaludoGenerico", "RemitenteSospechoso", "UsaAcortadorURL",
        "ExcesoDeEnlaces"
    ]

    df = pd.DataFrame(resultados, columns=columns)
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"✅ Análisis de características completado. Archivo generado: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso: python analizador_de_caracteristicas.py <archivo_de_entrada.txt> [archivo_de_salida.csv]")
        print("   Ejemplo: python analizador_de_caracteristicas.py mis_correos.txt resultados.csv")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "correos_analizados.csv"
        analizar_correos(input_file, output_file)

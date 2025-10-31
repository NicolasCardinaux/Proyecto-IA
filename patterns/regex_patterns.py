# Expresiones regulares para detectar errores comunes
ERRORS_PATTERN = r'\b(urjente|nesesita|actualisar|verificacion|hasido|disculpa|grasias|kiero|q|tmb|diculpa|vienbenido|nesesitas|porfavor|ud\.?)\b'

# Expresión regular para enlaces URL
LINKS_PATTERN = r'https?://[^\s/$.?#].[^\s]*'

# Expresión regular para emails
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Expresión regular para detectar saludos genéricos
GREETINGS_PATTERN = r'^(estimado cliente|querido usuario|apreciado cliente|dear customer|hola,|hi there|greetings|premium user|valued customer)'

# Expresión regular para detectar números de teléfono
PHONE_PATTERN = r'(\+\d{1,3}[-.]?)?\d{2,4}[-.]?\d{3,4}[-.]?\d{3,4}'

# Detecta palabras relacionadas a la solicitud de información sensible
SENSIBLE_PATTERN = r'(ingrese|introduzca|complete|rellene|proporcione).*?(contraseña|password|usuario|credencial|tarjeta|cuenta|dni)'

# Detecta presencia de símbolos excesivos.
SYMBOLS_PATTERN = r'[!¡?¿]{2,}'

# Detecta la presencia de información de dirección de la organización.
ADDRESS_PATTERN = r'(calle|avenida|av\.|número|nro|piso|departamento|depto|address|street|ave)'

# Detecta presencia de información de palabras comúnes en nombres de organizaciones.
CORP_PATTERN = r'(inc\.|llc|s\.a\.|corporation|company|corp|ltda)'

# Delimitadores de correos.
DELIMITERS_PATTERN = [r"From:", r"De:", r"Recibidos\n", r"Received:"]

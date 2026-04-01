import re

def extraer_tiempos(cuerpo_mail):
    # 1. Limpieza total de caracteres invisibles y ruidos de formato
    texto = str(cuerpo_mail).replace('\xa0', ' ').replace('\t', ' ')
    
    # 2. Usamos una técnica de "Lookbehind". 
    # Buscamos la FECHA que viene inmediatamente después de la palabra clave, 
    # sin importar qué símbolos haya en el medio (:, espacios, etc.)
    
    # Explicación:
    # START DATE.*? -> Busca la frase y salta cualquier cosa hasta...
    # (\d{2}-\d{2}-\d{2}.*?[AP]M) -> Captura la fecha y hora hasta el AM/PM
    
    patron_start = r"START DATE.*?(\d{2}-\d{2}-\d{2}\s+\d{1,2}:\d{2}\s+[AP]M)"
    patron_deadline = r"DEADLINE.*?(\d{2}-\d{2}-\d{2}\s+\d{1,2}:\d{2}\s+[AP]M)"
    
    start_match = re.search(patron_start, texto, re.DOTALL | re.IGNORECASE)
    deadline_match = re.search(patron_deadline, texto, re.DOTALL | re.IGNORECASE)
    
    # Extraemos los grupos
    start_raw = start_match.group(1).strip() if start_match else "No encontrado"
    deadline_raw = deadline_match.group(1).strip() if deadline_match else "No encontrado"
    
    return start_raw, deadline_raw
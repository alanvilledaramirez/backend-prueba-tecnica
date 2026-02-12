from src.domain.schemas.solicitud_schema import SolicitudCreate
from src.domain.models.solicitud_model import NivelRiesgo

EMAIL_BLACKLIST_DOMAINS = ["yopmail.com", "mailinator.com", "tempmail.com", "10minutemail.com", "temporal.com", "temp.com"]
PAISES_RESTRINGIDOS = ["Corea del Norte", "Iran", "Cuba", "Siria", "Rusia"]

def calcular_riesgo(datos: SolicitudCreate) -> tuple[int, NivelRiesgo]:
    score = 0
    
    #Regla del dominio en lista negra
    dominio = datos.email.split("@")[-1].lower()
    if dominio in EMAIL_BLACKLIST_DOMAINS:
        score += 30
        
    #validacion del pais restringido
    if datos.pais in PAISES_RESTRINGIDOS:
        score += 50
        
    #validacion de la longitud del nuermo de documento
    if len(datos.numero_documento) < 8:
        score += 20
        
    #validacion de clasificacion segun el score
    if score > 60:
        nivel = NivelRiesgo.ALTO
    elif score >= 31:
        nivel = NivelRiesgo.MEDIO
    else:
        nivel = NivelRiesgo.BAJO
        
    return score, nivel
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel

class EstadoSolicitud(str, Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    REQUIERE_INFO = "requiere_informacion"

class NivelRiesgo(str, Enum):
    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"

class Solicitud(SQLModel, table=True):
    __tablename__ = "solicitudes"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    nombre_completo: str
    email: str = Field(index=True)
    telefono: str
    pais: str
    
    tipo_documento: str
    numero_documento: str
    url_imagen: str
    
    estado: EstadoSolicitud = Field(default=EstadoSolicitud.PENDIENTE)
    
    score_riesgo: Optional[int] = Field(default=None)
    nivel_riesgo: Optional[NivelRiesgo] = Field(default=None)
    
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
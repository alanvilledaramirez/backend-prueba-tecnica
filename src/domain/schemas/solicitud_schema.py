import uuid
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from src.domain.models.solicitud_model import EstadoSolicitud, NivelRiesgo

class SolicitudCreate(BaseModel):
    nombre_completo: str
    email: EmailStr
    telefono: str
    pais: str
    tipo_documento: str
    numero_documento: str
    url_imagen: str
    estado: Optional[str] = "PENDIENTE"

class SolicitudRead(SolicitudCreate):
    id: uuid.UUID
    estado: EstadoSolicitud
    score_riesgo: Optional[float] = None
    nivel_riesgo: Optional[NivelRiesgo] = None
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)

class SolicitudUpdate(BaseModel):
    estado: EstadoSolicitud

    @field_validator('estado', mode='before')
    @classmethod
    def validar_estado(cls, v):
        valid_values = [e.value for e in EstadoSolicitud]
        if isinstance(v, str) and v not in valid_values:
            raise ValueError(f"Estado invalido. Opciones: {valid_values}")
        return v
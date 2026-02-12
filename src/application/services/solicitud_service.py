from sqlmodel import Session, select
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import DataError
import uuid

from src.domain.models.solicitud_model import Solicitud, EstadoSolicitud
from src.domain.schemas.solicitud_schema import SolicitudCreate
from src.domain.risk_engine.rules import calcular_riesgo
from src.infrastructure.mongo import get_audit_collection

class SolicitudService:
    def __init__(self, db: Session):
        self.db = db

    async def crear_solicitud(self, datos: SolicitudCreate) -> Solicitud:
        score, nivel = calcular_riesgo(datos)
        nueva_solicitud = Solicitud.model_validate(datos)
        
        nueva_solicitud.score_riesgo = score
        nueva_solicitud.nivel_riesgo = nivel
        
        self.db.add(nueva_solicitud)
        self.db.commit()
        self.db.refresh(nueva_solicitud)
        
        await self._registrar_log_mongo(
            nueva_solicitud, 
            "CREACION", 
            f"Solicitud creada con estado inicial: {nueva_solicitud.estado}"
        )
        
        return nueva_solicitud

    async def obtener_todas(self):
        statement = select(Solicitud).order_by(Solicitud.fecha_creacion.desc())
        results = self.db.exec(statement)
        return results.all()

    async def obtener_por_id(self, solicitud_id: uuid.UUID):
        solicitud = self.db.get(Solicitud, solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return solicitud

    async def actualizar_estado(self, solicitud_id: uuid.UUID, nuevo_estado: str):
        try:
            solicitud_db = self.db.get(Solicitud, solicitud_id)
            if not solicitud_db:
                raise HTTPException(status_code=404, detail="Solicitud no encontrada")

            solicitud_db.estado = nuevo_estado
            
            self.db.add(solicitud_db)
            self.db.commit()
            self.db.refresh(solicitud_db)

            await self._registrar_log_mongo(solicitud_db, "ACTUALIZAR_ESTADO", f"Estado: {nuevo_estado}")
            return solicitud_db

        except DataError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Estado invalido")

    async def _registrar_log_mongo(self, solicitud: Solicitud, accion: str, detalle: str):
        try:
            logs_collection = get_audit_collection()
            log_entry = {
                "solicitud_id": str(solicitud.id),
                "accion": accion,
                "detalle": detalle,
                "timestamp": datetime.utcnow()
            }
            await logs_collection.insert_one(log_entry)
        except Exception as e:
            print(f"Error al guardar log: {e}")
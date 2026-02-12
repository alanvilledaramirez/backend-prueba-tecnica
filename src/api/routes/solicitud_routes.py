from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from src.infrastructure.database import get_session
from src.application.services.solicitud_service import SolicitudService
from src.domain.schemas.solicitud_schema import SolicitudCreate, SolicitudRead, SolicitudUpdate
from src.infrastructure.mongo import get_audit_collection
import uuid

router = APIRouter()

def get_service(session: Session = Depends(get_session)) -> SolicitudService:
    return SolicitudService(session)

@router.get("/auditoria")
async def obtener_logs_auditoria():
    collection = get_audit_collection()
    cursor = collection.find().sort("timestamp", -1).limit(20)
    logs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if "timestamp" in doc:
            doc["timestamp"] = doc["timestamp"].isoformat()
        logs.append(doc)
    return logs

@router.post("/", response_model=SolicitudRead, status_code=201)
async def crear_solicitud(solicitud: SolicitudCreate, service: SolicitudService = Depends(get_service)):
    return await service.crear_solicitud(solicitud)

@router.get("/", response_model=List[SolicitudRead])
async def listar_solicitudes(service: SolicitudService = Depends(get_service)):
    return await service.obtener_todas()

@router.get("/{solicitud_id}", response_model=SolicitudRead)
async def obtener_detalle(solicitud_id: uuid.UUID, service: SolicitudService = Depends(get_service)):
    return await service.obtener_por_id(solicitud_id)

@router.put("/{solicitud_id}", response_model=SolicitudRead)
async def actualizar_estado_solicitud(solicitud_id: uuid.UUID, datos: SolicitudUpdate, service: SolicitudService = Depends(get_service)):
    return await service.actualizar_estado(solicitud_id, nuevo_estado=datos.estado)
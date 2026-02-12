import pytest
from unittest.mock import MagicMock, AsyncMock
import uuid

from src.application.services.solicitud_service import SolicitudService
from src.domain.schemas.solicitud_schema import SolicitudCreate
from src.domain.risk_engine.rules import calcular_riesgo
from src.domain.models.solicitud_model import NivelRiesgo, Solicitud

def test_motor_riesgo_pais_prohibido():
    datos = SolicitudCreate(
        nombre_completo="Usuario Prohibido",
        email="test@normal.com",
        telefono="12345678",
        pais="Iran",
        tipo_documento="PASAPORTE",
        numero_documento="999",
        url_imagen="laimage.jpog",
        estado="PENDIENTE"
    )
    
    score, nivel = calcular_riesgo(datos)
    
    assert score == 70
    assert nivel == NivelRiesgo.ALTO

@pytest.mark.asyncio
async def test_crear_solicitud_service_logic():
    mock_db = MagicMock()
    service = SolicitudService(mock_db)
    service._registrar_log_mongo = AsyncMock()

    datos_entrada = SolicitudCreate(
        nombre_completo="Alan Test",
        email="alan@test.com",
        telefono="5551234",
        pais="Mexico",
        tipo_documento="INE",
        numero_documento="12345678",
        url_imagen="laimagen.jpg",
        estado="aprobada"
    )

    resultado = await service.crear_solicitud(datos_entrada)

    assert resultado.nombre_completo == "Alan Test"
    assert resultado.estado == "aprobada"
    assert mock_db.add.called
    assert mock_db.commit.called
    assert service._registrar_log_mongo.called
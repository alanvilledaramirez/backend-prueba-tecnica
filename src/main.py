# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.infrastructure.database import init_db
from src.infrastructure.mongo import connect_to_mongo, close_mongo_connection
from src.api.routes import solicitud_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando app")
    init_db()
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="Prueba tecnica APIs", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(solicitud_routes.router, prefix="/api/v1/solicitudes", tags=["Solicitudes"])

@app.get("/")
def read_root():
    return {"message": "Todo chido"}
# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.infrastructure.database import init_db
from src.infrastructure.mongo import connect_to_mongo, close_mongo_connection
from src.api.routes import solicitud_routes
from fastapi import Request

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando app")
    init_db()
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="Prueba tecnica APIs", lifespan=lifespan)

@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

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
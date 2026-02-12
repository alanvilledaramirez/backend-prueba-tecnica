from sqlmodel import SQLModel, create_engine, Session
from src.config import settings
from src.domain.models.solicitud_model import Solicitud

engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
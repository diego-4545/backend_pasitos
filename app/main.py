from fastapi import FastAPI
from app.database import engine, Base
import app.models

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"mensaje": "API activa"}

@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}

from app.routers import ninos, padres, maestros, fechas, pagos, agenda

app.include_router(ninos.router)
app.include_router(padres.router)
app.include_router(maestros.router)
app.include_router(fechas.router)
app.include_router(pagos.router)
app.include_router(agenda.router)

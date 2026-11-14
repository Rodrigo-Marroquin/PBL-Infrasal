"""Servicio mock IMACASA - Inspección visual de defectos (CP1).

Endpoints:
  GET /health  -> 200 {"status": "ok"}           (sin autenticación)
  GET /info    -> 401 sin credenciales            (HTTP Basic Auth)
               -> 200 JSON equipo/estación/versión/timestamp con credenciales válidas
"""
import os
import secrets
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

TEAM = os.getenv("TEAM_NAME", "Equipo00")
STATION = os.getenv("STATION", "PC12 Inyectado")
VERSION = os.getenv("APP_VERSION", "1.0.0")
API_USER = os.getenv("API_USER", "imacasa")
API_PASSWORD = os.getenv("API_PASSWORD", "cambia-esta-clave")

app = FastAPI(
    title="IMACASA Mock Inspection Service",
    version=VERSION,
    docs_url=None,  # solo se exponen /health e /info
    redoc_url=None,
    openapi_url=None,
)
security = HTTPBasic(auto_error=False)


def verify(credentials: HTTPBasicCredentials | None = Depends(security)) -> str:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales requeridas o inválidas",
        headers={"WWW-Authenticate": 'Basic realm="imacasa"'},
    )
    if credentials is None:
        raise unauthorized
    # compare_digest evita ataques de temporización
    ok_user = secrets.compare_digest(credentials.username.encode(), API_USER.encode())
    ok_pass = secrets.compare_digest(credentials.password.encode(), API_PASSWORD.encode())
    if not (ok_user and ok_pass):
        raise unauthorized
    return credentials.username


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/info")
def info(_: str = Depends(verify)) -> dict:
    return {
        "equipo": TEAM,
        "estacion": STATION,
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

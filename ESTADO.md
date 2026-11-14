# Estado – Persona 4 (Docker, túnel y arquitectura) · PC12 Inyectado

## ✅ Hecho

| Entregable | Archivo | Va en la sección del reporte |
|---|---|---|
| API mock con `GET /health` (abierto) y `GET /info` (HTTP Basic, 401/200) | `app/main.py` | 5 |
| Dockerfile (Python 3.11 slim, usuario sin privilegios, healthcheck) | `Dockerfile` | 5 (evidencia: pegarlo tal cual) |
| Docker Compose: API + túnel ngrok con dominio estático | `docker-compose.yml` | 5 |
| Plantilla de variables (equipo, estación, credenciales, token) | `.env.example` | – |
| Justificación de autenticación y túnel (texto listo) | `README.md`, apartado 4 | 5 |
| Diagrama de arquitectura completo (3 estaciones, inferencia en edge) | `docs/arquitectura.png` / `.svg` | 2 |
| Texto de arquitectura + tabla de servicios justificados | `docs/arquitectura.md` | 2 |

Verificado localmente: `/health` → 200, `/info` sin credenciales → 401, con clave mala → 401, con credenciales → 200 + JSON.

La decisión **edge** se tomó con la sección 3 (EfficientAD-S ~2 ms, YOLO26-seg n/s).

**Túnel activo y probado desde internet** (14-nov): `https://finalize-ruckus-spirited.ngrok-free.dev` → `/health` 200, `/info` 401, `/info` con credenciales 200 + JSON. Credenciales de prueba: las tiene Persona 4 (van en la portada).

**Evidencias (sección 5)** en `docs/evidencias/`:
- `docker-curl.png` / `.txt`: `docker build`, `docker run`, `docker ps` (healthy) y los 3 `curl` contra el contenedor (200, 401, 200 + JSON). Se ejecutó en GitHub Codespaces porque Docker Desktop no arranca en la laptop de Persona 4 (WSL2).
- `tunel-curl.png` / `.txt`: los 3 `curl` contra la URL pública del túnel.

Las imágenes son la salida real de los comandos, renderizada desde los `.txt`.

## ⏳ Pendiente
- [ ] Confirmar el número de equipo (para el nombre del PDF y el campo `equipo` de `/info`).
- [ ] Día de la clase: Persona 4 levanta la API y el túnel 15 min antes. En su laptop la API corre con `run-local.ps1` (Python) mientras Docker Desktop no funcione ahí.

## 📌 Para el resto del equipo
- **Quien arma el PDF:** usar `docs/arquitectura.png` + `docs/arquitectura.md` (sección 2), y el Dockerfile + justificación del README (sección 5).
- **Persona 3:** el diagrama asume cámara de área con obturador global, iluminación difusa + rasante y marcador ArUco. Si eligen otra cosa, avisen para ajustarlo.
- **Persona 3 (UI):** la UI del diagrama incluye login, tiempo real, selector de 3 estaciones, historial filtrable y mapa de calor de EfficientAD.
- **Día de la clase:** el túnel debe estar activo; Persona 4 lo levanta 15 min antes y prueba los 3 `curl`.

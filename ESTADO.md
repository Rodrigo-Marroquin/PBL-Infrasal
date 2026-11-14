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

## ⏳ Pendiente (lo hace Persona 4)
- [ ] Levantar con Docker y túnel público (`docker compose up -d --build`).
- [ ] Capturas de los 3 `curl` (200, 401, 200 + JSON) → se suben a `docs/evidencias/`.
- [ ] Entregar a quien arma el PDF: **URL del túnel** y **credenciales** para la portada.

## 📌 Para el resto del equipo
- **Quien arma el PDF:** usar `docs/arquitectura.png` + `docs/arquitectura.md` (sección 2), y el Dockerfile + justificación del README (sección 5).
- **Persona 3:** el diagrama asume cámara de área con obturador global, iluminación difusa + rasante y marcador ArUco. Si eligen otra cosa, avisen para ajustarlo.
- **Persona 3 (UI):** la UI del diagrama incluye login, tiempo real, selector de 3 estaciones, historial filtrable y mapa de calor de EfficientAD.
- **Día de la clase:** el túnel debe estar activo; Persona 4 lo levanta 15 min antes y prueba los 3 `curl`.

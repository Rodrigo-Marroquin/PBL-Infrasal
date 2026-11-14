# Servicio mock IMACASA – PC12 Inyectado (Persona 4)

Servicio en Docker con dos endpoints, expuesto por túnel público (ngrok).

| Endpoint | Auth | Respuesta |
|---|---|---|
| `GET /health` | No | `200 {"status": "ok"}` |
| `GET /info` | HTTP Basic | sin credenciales → `401`; con credenciales → `200 {"equipo","estacion","version","timestamp"}` |

## 1. Preparar
1. Instalar **Docker Desktop**.
2. ngrok: `ngrok config add-authtoken TU_TOKEN` (una sola vez). Dominio estático: `finalize-ruckus-spirited.ngrok-free.dev`.
3. `cp .env.example .env` y llenar `API_PASSWORD` (el `.env` real no se sube al repo).

## 2. Ejecutar (comandos para el reporte)
```bash
docker compose up -d --build
ngrok http 8000 --url=finalize-ruckus-spirited.ngrok-free.dev
```
Plan B sin Docker: `.
un-local.ps1` + el mismo comando de ngrok.
Solo la API, sin compose:
```bash
docker build -t imacasa-mock:1.0.0 .
docker run -d --name imacasa-api -p 8000:8000 --env-file .env imacasa-mock:1.0.0
```

## 3. Pruebas (capturas para el reporte)
```bash
curl -i https://finalize-ruckus-spirited.ngrok-free.dev/health
curl -i https://finalize-ruckus-spirited.ngrok-free.dev/info
curl -i -u imacasa:TU-CLAVE https://finalize-ruckus-spirited.ngrok-free.dev/info
```
Esperado: 200, 401, 200 + JSON. Para la portada: **URL** `https://finalize-ruckus-spirited.ngrok-free.dev` y **credenciales** `-u imacasa:TU-CLAVE`.

## 4. Justificación (texto para el reporte)
**Esquema de autenticación – HTTP Basic sobre HTTPS.** Es el estándar más simple (RFC 7617) que el profesor puede probar con `curl -u usuario:clave`; el túnel termina TLS, así que las credenciales viajan cifradas. La comparación usa `secrets.compare_digest` (tiempo constante) y las credenciales se inyectan por variables de entorno, no están en la imagen. En producción se migraría a tokens JWT/OAuth2 con usuarios por rol (operador, supervisor de calidad).

**Túnel – ngrok con dominio estático.** El dominio gratuito de ngrok es fijo: la URL impresa en la portada del PDF sigue siendo válida aunque se reinicie el contenedor el día de la clase. Se descartó el *quick tunnel* de Cloudflare (`trycloudflare.com`) porque genera una URL aleatoria nueva en cada reinicio. Ngrok además da HTTPS automático y un panel de inspección (`localhost:4040`) útil para depurar en vivo. En producción en planta se usaría Cloudflare Tunnel con dominio propio + Cloudflare Access.

**Docker.** Imagen `python:3.11-slim`, usuario sin privilegios, `HEALTHCHECK` sobre `/health`, `restart: unless-stopped` para que se recupere sola. FastAPI + Uvicorn: ligero y el mismo stack que serviría la inferencia real.

## 5. Diagrama de arquitectura (borrador, Mermaid)
```mermaid
flowchart LR
  subgraph Planta["Planta IMACASA (edge)"]
    C1[Cámara PC08] --> E
    C2[Cámara PC10] --> E
    C3[Cámara PC12 Inyectado] --> E
    E["PC industrial edge<br/>captura + inferencia<br/>(Docker, GPU tipo Jetson)"]
  end
  E -- "HTTPS / túnel" --> API["API FastAPI<br/>(/health, /info, /inspecciones)"]
  E -- imagen --> S3[("Almacenamiento de objetos<br/>imágenes")]
  API --> DB[("PostgreSQL<br/>veredictos, defecto, confianza")]
  API --> UI["UI web<br/>login, tiempo real, 3 estaciones,<br/>historial filtrable"]
  S3 --> UI
```
Confirmado con la sección 3 (EfficientAD-S 2.2 ms, YOLO26-seg n/s): inferencia en **edge**. Diagrama final: `docs/arquitectura.png` (fuente `docs/arquitectura.svg`) y texto en `docs/arquitectura.md`.

## 6. Checklist día de la clase
- [ ] Laptop conectada a corriente, sin suspensión.
- [ ] `docker compose up -d` 15 min antes; probar los 3 `curl`.
- [ ] No cambiar la clave después de entregar el PDF.

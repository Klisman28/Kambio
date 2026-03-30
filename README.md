# Kambio

Sistema financiero web para control de divisas MXN/GTQ, libro mayor por cliente, control de caja, reportes y auditoría.

## Stack
- **Backend:** Python + FastAPI + SQLAlchemy + Alembic
- **Frontend:** Vue 3 + TypeScript + Vite + Pinia
- **Base de datos:** PostgreSQL

## Estructura
- `backend/` — API FastAPI
- `frontend/` — App Vue 3 (con tema comprado como base visual)
- `docs/` — PRD, arquitectura y tareas

## Documentación
- [`AGENTS.md`](./AGENTS.md) — reglas globales del proyecto
- [`CLAUDE.md`](./CLAUDE.md) — guía para Claude Code
- [`docs/PRD.md`](./docs/PRD.md) — product requirements
- [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) — decisiones técnicas y modelo de datos
- [`docs/TASKS.md`](./docs/TASKS.md) — backlog por fases

## Desarrollo rápido

```bash
docker compose up
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

## Fases
| Fase | Contenido | Estado |
|---|---|---|
| Fase 0 | Scaffold, Docker, auth base, integración del tema | 🔄 En progreso |
| Fase 1 | Clientes, transacciones, libro mayor | 🔲 Pendiente |
| Fase 2 | Caja, dashboard, reportes | 🔲 Pendiente |
| Fase 3 | Auditoría, exportaciones, hardening | 🔲 Pendiente |

# CLAUDE.md

Lee primero:
- AGENTS.md
- docs/PRD.md
- docs/ARCHITECTURE.md
- docs/TASKS.md

## Rol esperado
Actúa como arquitecto de software senior y desarrollador backend/frontend senior.

## Objetivo
Construir Finances con:
- backend FastAPI
- frontend Vue 3 + TypeScript
- MySQL
- tema comprado como base visual

## Reglas backend
- Usar FastAPI
- Versionar API desde el inicio: `/api/v1`
- Separar:
  - ORM models
  - Pydantic schemas
  - services
  - repositories
- Usar SQLAlchemy + Alembic
- Usar transacciones ACID para operaciones financieras
- Nunca persistir saldo editable de cliente
- Calcular saldo desde historial de transacciones

## Reglas frontend
- Usar Vue 3 + TypeScript + Vite
- Usar Pinia y Vue Router
- Mantener el tema en `frontend/src/theme`
- Crear lógica del sistema en `frontend/src/modules`
- No mezclar código demo del tema con la lógica del negocio
- No rehacer estilos base del tema sin necesidad

## Reglas de calidad
- Primero plan, luego cambios
- Mostrar archivos a tocar antes de cambios grandes
- Preferir cambios incrementales
- Al final de cada tarea, responder con:
  - resumen
  - archivos cambiados
  - riesgos
  - siguiente paso recomendado

## Módulos V1
- auth
- users/roles
- clients
- transactions
- ledger
- cash
- dashboard
- reports

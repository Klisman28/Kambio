# Finances — reglas globales del proyecto

## Contexto del producto
Sistema financiero web para:
- control de divisas MXN/GTQ
- libro mayor por cliente
- control de caja
- reportes
- auditoría básica

## Stack fijado
- Frontend: Vue 3 + TypeScript + Vite
- Backend: Python + FastAPI
- Base de datos: PostgreSQL
- ORM: SQLAlchemy
- Migraciones: Alembic
- Estado frontend: Pinia
- Router frontend: Vue Router

## Regla clave del frontend
- Ya existe un tema comprado.
- El tema es la base visual del sistema.
- No rehacer el frontend desde cero.
- Preservar layouts, navegación, assets y componentes útiles del tema.
- La lógica de negocio debe vivir en módulos propios del sistema.

## Reglas clave del negocio
- No existe tasa automática del sistema.
- Cada operación registra manualmente monto MXN, monto GTQ, comisión y opcionalmente tipo de cambio pactado.
- El saldo del cliente NO es editable manualmente.
- El saldo se calcula desde el historial de transacciones.
- No borrar transacciones financieras; usar anulación o estado.
- Solo puede haber una caja abierta a la vez.

## Reglas de ingeniería
- Antes de cambiar archivos, proponer un plan corto.
- Hacer cambios pequeños y revisables.
- No tocar secretos ni archivos `.env`.
- Si cambias contratos API, actualizar `docs/ARCHITECTURE.md`.
- Si cambias alcance o módulos, actualizar `docs/PRD.md` y `docs/TASKS.md`.
- Si tocas frontend, respetar la separación:
  - `frontend/src/theme` = tema comprado
  - `frontend/src/modules` = lógica del sistema

## Estructura objetivo
- backend/
- frontend/
- docs/

## Orden de trabajo
1. Leer `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`
2. Proponer plan
3. Esperar aprobación si el cambio es estructural
4. Implementar
5. Ejecutar validaciones
6. Documentar lo cambiado

## Fase inicial
- Fase 0: scaffold del proyecto, Docker Compose dev, auth base, integración del tema
- Fase 1: clientes, transacciones, libro mayor
- Fase 2: caja, dashboard, reportes
- Fase 3: auditoría, exportaciones, hardening

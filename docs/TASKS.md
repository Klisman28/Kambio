# TASKS — Kambio

**Versión:** 0.1-draft  
**Fecha:** 2026-03-29  
**Convención de estado:** 🔲 Pendiente | 🔄 En progreso | ✅ Hecho | ⏸ Bloqueado

---

## FASE 0 — Scaffold + Auth base + Integración de tema

> Objetivo: entorno de desarrollo funcional con autenticación end-to-end.

### 0.1 Documentación base

| ID | Tarea | Estado | Notas |
|---|---|---|---|
| T-0.1.1 | Escribir `docs/PRD.md` con alcance V1, módulos y reglas de negocio | ✅ Hecho | |
| T-0.1.2 | Escribir `docs/ARCHITECTURE.md` con modelo de datos y endpoints | ✅ Hecho | |
| T-0.1.3 | Escribir `docs/TASKS.md` (este archivo) con backlog por fases | ✅ Hecho | |
| T-0.1.4 | Resolver consistencia de nombre: adoptar **Kambio** en toda la documentación | ✅ Hecho | README y docs actualizados |

### 0.2 Infraestructura

| ID | Tarea | Estado | Notas |
|---|---|---|---|
| T-0.2.1 | Crear `docker-compose.yml` con mysql + backend + frontend | 🔲 Pendiente | |
| T-0.2.2 | Crear `backend/Dockerfile` con hot reload | 🔲 Pendiente | |
| T-0.2.3 | Crear `frontend/Dockerfile` con hot reload | 🔲 Pendiente | |
| T-0.2.4 | Crear `backend/.env.example` con todas las variables requeridas | 🔲 Pendiente | |
| T-0.2.5 | Crear `frontend/.env.example` con `VITE_API_BASE_URL` | 🔲 Pendiente | |

### 0.3 Backend — Scaffold

| ID | Tarea | Estado | Notas |
|---|---|---|---|
| T-0.3.1 | Inicializar proyecto FastAPI con estructura `app/` | 🔲 Pendiente | |
| T-0.3.2 | Configurar `app/core/config.py` con pydantic-settings | 🔲 Pendiente | |
| T-0.3.3 | Configurar `app/db/base.py` y `app/db/session.py` (SQLAlchemy 2) | 🔲 Pendiente | |
| T-0.3.4 | Crear `requirements.txt` con dependencias fijadas | 🔲 Pendiente | |
| T-0.3.5 | Inicializar Alembic y crear primera migración vacía | 🔲 Pendiente | |
| T-0.3.6 | Añadir endpoint `GET /api/v1/health` | 🔲 Pendiente | |
| T-0.3.7 | Configurar CORS para `localhost:5173` en dev | 🔲 Pendiente | |

### 0.4 Backend — Auth

| ID | Tarea | Estado | Notas |
|---|---|---|---|
| T-0.4.1 | Crear modelo ORM `users` con campos según ARCHITECTURE.md | 🔲 Pendiente | |
| T-0.4.2 | Crear migración Alembic para tabla `users` | 🔲 Pendiente | |
| T-0.4.3 | Implementar `app/core/security.py` (JWT + bcrypt) | 🔲 Pendiente | |
| T-0.4.4 | Implementar `user_repo.py` con `get_by_email` | 🔲 Pendiente | |
| T-0.4.5 | Implementar `auth_service.py` con login y verificación | 🔲 Pendiente | |
| T-0.4.6 | Implementar `POST /api/v1/auth/login` | 🔲 Pendiente | |
| T-0.4.7 | Implementar `GET /api/v1/auth/me` con dependency de usuario autenticado | 🔲 Pendiente | |
| T-0.4.8 | Crear usuario admin semilla (`seed`) para desarrollo | 🔲 Pendiente | |

### 0.5 Frontend — Scaffold + Integración del tema

| ID | Tarea | Estado | Notas |
|---|---|---|---|
| T-0.5.1 | Evaluar estructura del tema comprado e identificar layouts reutilizables | 🔲 Pendiente | **BLOQUEANTE: el tema debe estar disponible primero** |
| T-0.5.2 | Inicializar proyecto Vite + Vue 3 + TypeScript si no existe | 🔲 Pendiente | |
| T-0.5.3 | Copiar tema a `frontend/src/theme/` sin modificar | 🔲 Pendiente | |
| T-0.5.4 | Crear `frontend/src/modules/` con estructura base de módulos | 🔲 Pendiente | |
| T-0.5.5 | Instalar y configurar Pinia | 🔲 Pendiente | |
| T-0.5.6 | Instalar y configurar Vue Router con rutas base | 🔲 Pendiente | |
| T-0.5.7 | Crear `api/http.ts` con axios + interceptor de token | 🔲 Pendiente | |

### 0.6 Frontend — Auth

| ID | Tarea | Estado | Notas |
|---|---|---|---|
| T-0.6.1 | Crear `authStore.ts` (Pinia): token, usuario, login, logout | 🔲 Pendiente | |
| T-0.6.2 | Crear `useAuth.ts` composable | 🔲 Pendiente | |
| T-0.6.3 | Adaptar `LoginPage.vue` usando el layout del tema | 🔲 Pendiente | |
| T-0.6.4 | Implementar navigation guard en el router | 🔲 Pendiente | |
| T-0.6.5 | Verificar flujo completo: login → dashboard → logout → redirect a /login | 🔲 Pendiente | |

---

## FASE 1 — Clientes + Transacciones + Libro Mayor

> Prerequisito: Fase 0 ✅

### 1.1 Clientes

| ID | Tarea | Estado |
|---|---|---|
| T-1.1.1 | Modelo ORM `clients` + migración | 🔲 Pendiente |
| T-1.1.2 | Schema Pydantic + CRUD de clientes | 🔲 Pendiente |
| T-1.1.3 | Endpoints GET/POST/PATCH `/api/v1/clients` | 🔲 Pendiente |
| T-1.1.4 | Página lista de clientes (frontend) | 🔲 Pendiente |
| T-1.1.5 | Formulario nuevo/editar cliente | 🔲 Pendiente |
| T-1.1.6 | Vista perfil de cliente | 🔲 Pendiente |

### 1.2 Transacciones

| ID | Tarea | Estado |
|---|---|---|
| T-1.2.1 | Modelo ORM `transactions` + migración | 🔲 Pendiente |
| T-1.2.2 | Schema Pydantic + validaciones | 🔲 Pendiente |
| T-1.2.3 | `transaction_service.py` con reglas de negocio | 🔲 Pendiente |
| T-1.2.4 | Endpoints CRUD + cancel `/api/v1/transactions` | 🔲 Pendiente |
| T-1.2.5 | Formulario registro de transacción (frontend) | 🔲 Pendiente |
| T-1.2.6 | Lista de transacciones con filtros básicos | 🔲 Pendiente |
| T-1.2.7 | Flujo de anulación de transacción | 🔲 Pendiente |

### 1.3 Libro Mayor (Ledger)

| ID | Tarea | Estado |
|---|---|---|
| T-1.3.1 | `ledger_service.py`: cálculo de saldo desde historial | ✅ Hecho |
| T-1.3.2 | Endpoints `GET /api/v1/ledger/{client_id}` e `/balance` | ✅ Hecho |
| T-1.3.3 | Vista de libro mayor por cliente (frontend) | ✅ Hecho |
| T-1.3.4 | Tests unitarios de cálculo de saldo | ✅ Hecho |

---

## FASE 2 — Caja + Dashboard + Reportes

> Prerequisito: Fase 1 ✅

### 2.1 Caja

| ID | Tarea | Estado |
|---|---|---|
| T-2.1.1 | Modelo ORM `cash_sessions` + migración | ✅ Hecho |
| T-2.1.2 | `cash_service.py` con regla de caja única | ✅ Hecho |
| T-2.1.3 | Endpoints open/close/current/history | ✅ Hecho |
| T-2.1.4 | Vista apertura y cierre de caja (frontend) | ✅ Hecho |
| T-2.1.5 | Indicador de estado de caja en header/dashboard | ✅ Hecho |

### 2.2 Dashboard

| ID | Tarea | Estado |
|---|---|---|
| T-2.2.1 | Endpoint de métricas del día | 🔲 Pendiente |
| T-2.2.2 | Página dashboard con KPIs: operaciones, saldo total, caja activa | 🔲 Pendiente |
| T-2.2.3 | Tabla de últimas transacciones en dashboard | 🔲 Pendiente |

### 2.3 Reportes

| ID | Tarea | Estado |
|---|---|---|
| T-2.3.1 | Endpoint `GET /api/v1/reports/transactions` con filtros | 🔲 Pendiente |
| T-2.3.2 | Endpoint `GET /api/v1/reports/cash-summary` | 🔲 Pendiente |
| T-2.3.3 | Página de reportes con filtros de fecha y cliente (frontend) | 🔲 Pendiente |
| T-2.3.4 | Exportación a CSV básica | 🔲 Pendiente |

---

## FASE 3 — Auditoría + Exportaciones + Hardening

> Prerequisito: Fase 2 ✅

| ID | Tarea | Estado |
|---|---|---|
| T-3.1 | Modelo ORM `audit_logs` + migración | 🔲 Pendiente |
| T-3.2 | Middleware o hook de auditoría en servicios críticos | 🔲 Pendiente |
| T-3.3 | Endpoint y vista de log de auditoría (solo admin) | 🔲 Pendiente |
| T-3.4 | Exportación a PDF de reportes | 🔲 Pendiente |
| T-3.5 | Rate limiting en API | 🔲 Pendiente |
| T-3.6 | Revisión de permisos y edge cases de seguridad | 🔲 Pendiente |
| T-3.7 | Tests de integración end-to-end | 🔲 Pendiente |
| T-3.8 | Documentación de despliegue en producción | 🔲 Pendiente |

---

## Dependencias críticas bloqueantes

| Bloqueante | Tarea bloqueada | Acción requerida |
|---|---|---|
| Tema comprado no disponible | T-0.5.1 al T-0.6.3 | El usuario debe proveer los archivos del tema |
| Docker Desktop instalado | T-0.2.1 al T-0.2.3 | Confirmar instalación en el equipo |
| Instancia MySQL accesible | T-0.3.5 al T-0.4.8 | Via Docker o local |

---

## Notas de proceso

- **Una tarea por PR** siempre que sea posible
- **Migración Alembic** por cada cambio de modelo — nunca editar migraciones existentes
- **Al cerrar una tarea**, actualizar este archivo y hacer commit
- **Antes de iniciar una fase nueva**, todas las CAs de la fase anterior deben estar en verde

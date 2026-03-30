# ARCHITECTURE — Kambio

**Versión:** 0.1-draft  
**Fecha:** 2026-03-29  
**Estado:** Fase 0 — Documental

---

## 1. Stack tecnológico

| Capa | Tecnología | Versión mínima |
|---|---|---|
| Frontend | Vue 3 + TypeScript + Vite | Vue 3.4+, Vite 5+ |
| Estado UI | Pinia | 2+ |
| Router UI | Vue Router | 4+ |
| Backend | Python + FastAPI | Python 3.11+, FastAPI 0.110+ |
| ORM | SQLAlchemy | 2+ |
| Migraciones | Alembic | 1.13+ |
| Base de datos | MySQL | 8.0+ |
| Auth | JWT (python-jose) + bcrypt | — |
| Contenedores | Docker + Docker Compose | — |
| Variables de entorno | pydantic-settings | 2+ |

---

## 2. Estructura de directorios

```
Kambio/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── core/
│   │   │   ├── config.py            # Settings via pydantic-settings
│   │   │   └── security.py          # JWT helpers, password hashing
│   │   ├── db/
│   │   │   ├── base.py              # SQLAlchemy declarative base
│   │   │   └── session.py           # Engine, SessionLocal, get_db dep
│   │   ├── models/                  # ORM models (SQLAlchemy)
│   │   │   ├── user.py
│   │   │   ├── client.py
│   │   │   ├── transaction.py
│   │   │   ├── cash.py
│   │   │   └── audit_log.py
│   │   ├── schemas/                 # Pydantic I/O schemas
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── client.py
│   │   │   ├── transaction.py
│   │   │   └── cash.py
│   │   ├── repositories/            # DB queries (sin lógica de negocio)
│   │   │   ├── user_repo.py
│   │   │   ├── client_repo.py
│   │   │   ├── transaction_repo.py
│   │   │   └── cash_repo.py
│   │   ├── services/                # Lógica de negocio + reglas
│   │   │   ├── auth_service.py
│   │   │   ├── client_service.py
│   │   │   ├── transaction_service.py
│   │   │   ├── ledger_service.py
│   │   │   └── cash_service.py
│   │   └── api/
│   │       └── v1/
│   │           ├── router.py        # Agrega todos los sub-routers
│   │           ├── auth.py
│   │           ├── users.py
│   │           ├── clients.py
│   │           ├── transactions.py
│   │           ├── ledger.py
│   │           ├── cash.py
│   │           └── reports.py
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── .env.example                 # Variables sin valores reales
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── theme/                   # ⚠️ Tema comprado — NO modificar
│   │   │   ├── assets/
│   │   │   ├── layouts/
│   │   │   └── components/
│   │   ├── modules/                 # Lógica del sistema Kambio
│   │   │   ├── auth/
│   │   │   │   ├── composables/
│   │   │   │   │   └── useAuth.ts
│   │   │   │   ├── stores/
│   │   │   │   │   └── authStore.ts
│   │   │   │   └── pages/
│   │   │   │       └── LoginPage.vue
│   │   │   ├── clients/
│   │   │   ├── transactions/
│   │   │   ├── ledger/
│   │   │   ├── cash/
│   │   │   ├── dashboard/
│   │   │   └── reports/
│   │   ├── router/
│   │   │   └── index.ts             # Rutas + guards de auth
│   │   ├── api/
│   │   │   └── http.ts              # axios instance con base URL + interceptors
│   │   └── main.ts
│   ├── public/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── .env.example
│   └── Dockerfile
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── TASKS.md
│
├── docker-compose.yml               # MySQL + backend + frontend
├── AGENTS.md
├── CLAUDE.md
└── README.md
```

---

## 3. Modelo de datos propuesto

### 3.1 `users`

| Campo | Tipo | Notas |
|---|---|---|
| `id` | UUID PK | |
| `email` | VARCHAR UNIQUE | |
| `hashed_password` | VARCHAR | bcrypt |
| `full_name` | VARCHAR | |
| `role` | ENUM(`admin`, `operator`, `viewer`) | |
| `is_active` | BOOLEAN | default true |
| `created_at` | TIMESTAMP | |
| `updated_at` | TIMESTAMP | |

### 3.2 `clients`

| Campo | Tipo | Notas |
|---|---|---|
| `id` | UUID PK | |
| `full_name` | VARCHAR | |
| `phone` | VARCHAR | nullable |
| `email` | VARCHAR | nullable |
| `notes` | TEXT | nullable |
| `is_active` | BOOLEAN | default true |
| `created_at` | TIMESTAMP | |
| `updated_at` | TIMESTAMP | |

### 3.3 `transactions`

| Campo | Tipo | Notas |
|---|---|---|
| `id` | UUID PK | |
| `client_id` | UUID FK → clients | |
| `user_id` | UUID FK → users | operador que registra |
| `type` | ENUM(`ENTRADA`, `SALIDA`) | |
| `monto_mxn` | NUMERIC(18,4) | nullable |
| `monto_gtq` | NUMERIC(18,4) | nullable |
| `comision` | NUMERIC(18,4) | default 0 |
| `tipo_cambio_pactado` | NUMERIC(18,6) | nullable |
| `status` | ENUM(`ACTIVA`, `ANULADA`) | default ACTIVA |
| `notes` | TEXT | nullable |
| `cancelled_reason` | TEXT | nullable |
| `cancelled_by` | UUID FK → users | nullable |
| `cancelled_at` | TIMESTAMP | nullable |
| `created_at` | TIMESTAMP | |

### 3.4 `cash_sessions` (Caja)

| Campo | Tipo | Notas |
|---|---|---|
| `id` | UUID PK | |
| `opened_by` | UUID FK → users | |
| `closed_by` | UUID FK → users | nullable |
| `status` | ENUM(`ABIERTA`, `CERRADA`) | |
| `monto_apertura_mxn` | NUMERIC(18,4) | |
| `monto_apertura_gtq` | NUMERIC(18,4) | |
| `monto_cierre_mxn` | NUMERIC(18,4) | nullable |
| `monto_cierre_gtq` | NUMERIC(18,4) | nullable |
| `opened_at` | TIMESTAMP | |
| `closed_at` | TIMESTAMP | nullable |
| `notes` | TEXT | nullable |

### 3.5 `audit_logs`

| Campo | Tipo | Notas |
|---|---|---|
| `id` | UUID PK | |
| `user_id` | UUID FK → users | nullable (sistema) |
| `action` | VARCHAR | ej. `TRANSACTION_CANCEL`, `CASH_CLOSE` |
| `entity` | VARCHAR | ej. `transactions`, `cash_sessions` |
| `entity_id` | UUID | |
| `payload` | JSONB | snapshot del cambio |
| `created_at` | TIMESTAMP | |

---

## 4. Contratos de API — `/api/v1`

### Auth
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/auth/login` | Retorna `access_token` JWT |
| GET | `/api/v1/auth/me` | Usuario autenticado (requiere token) |
| POST | `/api/v1/auth/logout` | Invalida sesión (cliente elimina token) |

### Users
| Método | Ruta | Acceso |
|---|---|---|
| GET | `/api/v1/users` | admin |
| POST | `/api/v1/users` | admin |
| GET | `/api/v1/users/{id}` | admin |
| PATCH | `/api/v1/users/{id}` | admin |
| DELETE | `/api/v1/users/{id}` | admin (soft delete) |

### Clients
| Método | Ruta | Acceso |
|---|---|---|
| GET | `/api/v1/clients` | operator, admin |
| POST | `/api/v1/clients` | operator, admin |
| GET | `/api/v1/clients/{id}` | operator, admin |
| PATCH | `/api/v1/clients/{id}` | operator, admin |

### Transactions
| Método | Ruta | Acceso |
|---|---|---|
| GET | `/api/v1/transactions` | operator, admin |
| POST | `/api/v1/transactions` | operator, admin |
| GET | `/api/v1/transactions/{id}` | operator, admin |
| POST | `/api/v1/transactions/{id}/cancel` | operator, admin |

### Ledger
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/ledger/{client_id}` | Historial de transacciones del cliente |
| GET | `/api/v1/ledger/{client_id}/balance` | Saldo calculado en MXN y GTQ |

### Cash
| Método | Ruta | Acceso |
|---|---|---|
| GET | `/api/v1/cash/current` | Estado de la caja actual |
| POST | `/api/v1/cash/open` | operator, admin |
| POST | `/api/v1/cash/close` | operator, admin |
| GET | `/api/v1/cash/history` | admin |

### Reports
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/reports/transactions` | Filtros: `from`, `to`, `client_id`, `status` |
| GET | `/api/v1/reports/cash-summary` | Resumen de cajas cerradas |

### Health
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/health` | `{"status": "ok"}` — sin auth |

---

## 5. Autenticación y seguridad

- **JWT Bearer token** en header `Authorization: Bearer <token>`
- Token expira en **60 minutos** (configurable)
- Contraseñas hasheadas con **bcrypt** (cost factor 12)
- Roles evaluados en cada endpoint mediante dependency de FastAPI
- CORS configurado para solo aceptar el dominio del frontend
- Ningún endpoint (excepto `/health` y `/auth/login`) es público

---

## 6. Separación frontend: theme vs modules

```
frontend/src/
├── theme/          # Tema comprado — zona congelada
│   ├── assets/     # Imágenes, fuentes, íconos del tema
│   ├── layouts/    # Layouts base (sidebar, header, etc.)
│   └── components/ # Componentes UI genéricos del tema
│
└── modules/        # Kambio — zona de negocio
    ├── auth/       # Login, store de sesión, guard
    ├── clients/    # CRUD clientes
    ├── transactions/
    ├── ledger/
    ├── cash/
    ├── dashboard/
    └── reports/
```

**Regla:** ningún archivo en `modules/` importa directamente desde `theme/`. La comunicación se da únicamente a través de los layouts y slots del tema.

---

## 7. Docker Compose — entorno de desarrollo

```yaml
services:
  mysql:
    image: mysql:8.0
    ports: ["3306:3306"]
    volumes: [mysql_data:/var/lib/mysql]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [mysql]
    volumes: [./backend:/app]   # hot reload

  frontend:
    build: ./frontend
    ports: ["5173:5173"]
    volumes: [./frontend:/app]  # hot reload
```

---

## 8. Decisiones de arquitectura

| ID | Decisión | Alternativa descartada | Razón |
|---|---|---|---|
| AD-1 | Saldo calculado, no persistido | Campo `balance` en `clients` | Garantiza consistencia con el historial de transacciones |
| AD-2 | Anulación en vez de borrado | `DELETE` físico | Trazabilidad y auditoría financiera |
| AD-3 | Caja única global | Múltiples cajas | Simplifica V1; se puede extender en V2 |
| AD-4 | UUID como PK | Integer autoincrement | Seguridad (no enumerable), preparación para multi-tenant |
| AD-5 | NUMERIC(18,4) para montos | FLOAT | Precisión decimal sin errores de punto flotante |
| AD-6 | Separación repo/service/schema | Lógica en routers | Testabilidad y separación de responsabilidades |

---

## 9. Riesgos técnicos

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| RT-1 | El tema comprado no es compatible con la estructura de módulos propuesta | Media | Alto | Evaluar el tema antes de iniciar frontend |
| RT-2 | Errores de precisión en cálculo de saldo con NUMERIC | Baja | Alto | Tests unitarios de ledger_service con casos extremos |
| RT-3 | Condición de carrera al abrir dos cajas simultáneas | Media | Alto | Lock a nivel de base de datos + transacción ACID |
| RT-4 | JWT sin blacklist = token válido tras logout | Media | Medio | Usar short TTL (60 min) + blacklist Redis en V2 |
| RT-5 | Migraciones Alembic en conflicto entre ramas | Baja | Medio | Convención: una migración por PR |

---

## 10. Changelog

| Fecha | Versión | Cambio |
|---|---|---|
| 2026-03-29 | 0.1 | Documento inicial — Fase 0 documental |

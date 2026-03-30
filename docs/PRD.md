# PRD — Kambio

> Sistema financiero web para control de divisas MXN/GTQ, libro mayor por cliente, control de caja, reportes y auditoría básica.

**Versión:** 0.1-draft  
**Fecha:** 2026-03-29  
**Estado:** Fase 0 — Documental

---

## 1. Nombre del producto

| Campo | Valor |
|---|---|
| Nombre de producto | **Kambio** |
| Nombre de repositorio | `Klisman28/Kambio` |
| Directorio de trabajo | `c:\dev\Finances` (nombre local, no afecta al producto) |
| Versión objetivo inicial | V1 |

---

## 2. Contexto y problema

Kambio resuelve la operación diaria de una casa de cambio o negocio que opera con dos divisas (MXN y GTQ). El operador necesita:

- Registrar transacciones de clientes en MXN y GTQ
- Consultar el saldo y libro mayor de cada cliente
- Controlar una caja única por turno
- Generar reportes básicos de operación
- Tener trazabilidad y auditoría de todas las acciones

**Raíz del problema:** las operaciones se hacen en hojas de cálculo o sistemas genéricos que no imponen las reglas del negocio (tipo de cambio manual, caja única, saldo calculado).

---

## 3. Usuarios del sistema

| Rol | Descripción |
|---|---|
| `admin` | Acceso total. Configura usuarios, revisa auditoría, cierra cajas forzadas |
| `operator` | Registra transacciones, abre/cierra caja, consulta libro mayor |
| `viewer` | Solo consulta — sin escritura |

---

## 4. Alcance V1

### ✅ Incluido en V1

| Módulo | Descripción |
|---|---|
| **Auth** | Login con JWT, roles, sesión |
| **Users** | CRUD de usuarios con rol |
| **Clients** | Registro y perfil de clientes |
| **Transactions** | Registro manual MXN + GTQ + comisión + tipo de cambio pactado |
| **Ledger** | Libro mayor por cliente, saldo calculado desde historial |
| **Cash** | Control de caja: apertura, cierre, resumen del turno |
| **Dashboard** | Métricas del día: movimientos, saldo total, caja activa |
| **Reports** | Reporte de transacciones por rango de fecha y cliente |

### ❌ Fuera de V1

- Tasa de cambio automática o conectada a API externa
- Múltiples cajas simultáneas
- Móvil / PWA
- Importación masiva de transacciones
- Notificaciones / alertas automáticas
- Módulo contable completo (no es el alcance)

---

## 5. Reglas de negocio

### 5.1 Transacciones

1. Cada transacción registra: `monto_mxn`, `monto_gtq`, `comision`, y opcionalmente `tipo_cambio_pactado`.
2. No existe tipo de cambio automático del sistema — el operador lo ingresa manualmente en cada operación.
3. Las transacciones **nunca se borran**. Se anulan con estado `ANULADA` y se registra el motivo.
4. Una transacción anulada genera un registro de auditoría.

### 5.2 Saldo de cliente

5. El saldo del cliente **no es un campo editable** en la base de datos.
6. El saldo se **calcula en tiempo real** desde el historial completo de transacciones activas.
7. `saldo = SUM(entradas) - SUM(salidas)` en cada divisa.

### 5.3 Caja

8. Solo puede existir **una caja abierta a la vez** en todo el sistema.
9. Para abrir una nueva caja, la anterior debe estar cerrada.
10. Al cerrar caja: se registra monto de apertura, monto de cierre, total de operaciones y diferencia.
11. Solo `admin` puede forzar el cierre de una caja no propia.

### 5.4 Roles y permisos

12. Un usuario sin autenticación no puede acceder a ninguna ruta del sistema.
13. Los `viewer` no pueden crear ni modificar ningún recurso.
14. Solo `admin` puede crear/desactivar usuarios.

---

## 6. Criterios de aceptación — Fase 0

| ID | Criterio |
|---|---|
| CA-0.1 | El entorno de desarrollo levanta con `docker compose up` sin errores |
| CA-0.2 | El backend responde en `http://localhost:8000/api/v1/health` con `{"status": "ok"}` |
| CA-0.3 | El endpoint `POST /api/v1/auth/login` devuelve un JWT válido |
| CA-0.4 | El endpoint `GET /api/v1/auth/me` retorna datos del usuario autenticado |
| CA-0.5 | El frontend carga en `http://localhost:5173` mostrando la pantalla de login del tema |
| CA-0.6 | Login exitoso redirige al dashboard protegido |
| CA-0.7 | Ruta sin autenticación redirige a `/login` |
| CA-0.8 | Las migraciones de Alembic corren sin error (`alembic upgrade head`) |

---

## 7. Criterios de aceptación — V1 completa

| ID | Módulo | Criterio |
|---|---|---|
| CA-1.1 | Clients | Se puede crear, editar y listar clientes |
| CA-1.2 | Transactions | Se registra una transacción con MXN, GTQ, comisión y tipo de cambio opcional |
| CA-1.3 | Ledger | El saldo del cliente refleja correctamente todas sus transacciones activas |
| CA-1.4 | Ledger | Anular una transacción actualiza el saldo sin borrar el registro |
| CA-1.5 | Cash | No se puede abrir una segunda caja con una ya activa |
| CA-1.6 | Cash | El cierre de caja genera un resumen del turno |
| CA-1.7 | Reports | Se puede exportar un listado de transacciones filtradas por fecha y cliente |
| CA-1.8 | Auth | Un token expirado no da acceso a ningún endpoint protegido |

---

## 8. Fases del proyecto

| Fase | Contenido | Estado |
|---|---|---|
| **Fase 0** | Scaffold, Docker Compose, auth base, integración del tema | 🔲 Pendiente |
| **Fase 1** | Clientes, transacciones, libro mayor | 🔲 Pendiente |
| **Fase 2** | Caja, dashboard, reportes | 🔲 Pendiente |
| **Fase 3** | Auditoría, exportaciones, hardening | 🔲 Pendiente |

---

## 9. Glosario

| Término | Definición |
|---|---|
| MXN | Peso mexicano |
| GTQ | Quetzal guatemalteco |
| Caja | Registro de turno operativo con apertura y cierre |
| Libro mayor | Historial de todas las transacciones de un cliente |
| Anulación | Cancelación de transacción sin borrar el registro físico |
| Tipo de cambio pactado | Valor MXN/GTQ acordado manualmente para esa operación |

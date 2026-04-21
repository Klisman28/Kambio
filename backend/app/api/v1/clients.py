import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ledger_entry import Currency
from app.models.user import User
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.schemas.ledger import BalanceOut, LedgerGroupedResponse, LedgerResponse
from app.services.auth_service import get_current_user
from app.services.client_service import ClientService
from app.services.ledger_service import LedgerService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientOut, status_code=201, summary="Crear cliente")
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClientService(db).create(payload, current_user)


@router.get("", response_model=List[ClientOut], summary="Listar clientes")
def list_clients(
    q: Optional[str] = Query(None, description="Buscar por nombre"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return ClientService(db).list(q=q, skip=skip, limit=limit)


@router.get("/{client_id}", response_model=ClientOut, summary="Obtener cliente")
def get_client(
    client_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return ClientService(db).get_or_404(client_id)


@router.patch("/{client_id}", response_model=ClientOut, summary="Actualizar cliente")
def update_client(
    client_id: UUID,
    payload: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClientService(db).update(client_id, payload, current_user)


# ── Libro mayor y saldo (sub-recursos del cliente) ──────────────────────────

@router.get(
    "/{client_id}/balance",
    response_model=BalanceOut,
    summary="Saldo actual del cliente",
    description=(
        "Retorna la posición financiera del cliente por divisa con interpretación semántica. "
        "Si se provee `reference_exchange_rate` (MXN por 1 GTQ), se incluyen "
        "`equivalent_in_mxn` y `equivalent_in_gtq` como referencia visual únicamente — "
        "NO son saldo oficial y no alteran `raw_balance` ni `position`."
    ),
)
def get_balance(
    client_id: UUID,
    reference_exchange_rate: Optional[Decimal] = Query(
        None,
        gt=0,
        description="Tasa de referencia MXN/GTQ para equivalencia visual (no oficial)",
    ),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    ClientService(db).get_or_404(client_id)  # valida existencia
    return LedgerService(db).get_balance(client_id, reference_exchange_rate=reference_exchange_rate)


@router.get(
    "/{client_id}/ledger",
    response_model=LedgerResponse,
    summary="Libro mayor del cliente",
    description=(
        "Retorna el historial de movimientos del cliente con contexto de transacción. "
        "Solo incluye entradas de transacciones ACTIVE. "
        "CREDIT (+) = dinero que entra al cliente. DEBIT (−) = dinero que sale. "
        "El balance siempre se calcula desde el historial, nunca se almacena."
    ),
)
def get_ledger(
    client_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    currency: Optional[Currency] = Query(None, description="Filtrar por divisa: MXN o GTQ"),
    date_from: Optional[datetime.date] = Query(None, description="Desde fecha (YYYY-MM-DD)"),
    date_to: Optional[datetime.date] = Query(None, description="Hasta fecha (YYYY-MM-DD)"),
    reference_exchange_rate: Optional[Decimal] = Query(
        None,
        gt=0,
        description="Tasa de referencia MXN/GTQ para equivalencia visual en el saldo (no oficial)",
    ),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if date_from and date_to and date_to < date_from:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="date_to debe ser mayor o igual a date_from",
        )
    ClientService(db).get_or_404(client_id)
    return LedgerService(db).get_ledger(
        client_id,
        currency=currency,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit,
        reference_exchange_rate=reference_exchange_rate,
    )


@router.get(
    "/{client_id}/ledger-summary",
    response_model=LedgerGroupedResponse,
    summary="Libro mayor agrupado por transacción",
    description=(
        "Vista tipo Excel del libro mayor: **una fila por transacción** con columnas "
        "separadas para egreso/ingreso por divisa.\n\n"
        "**Diferencia con `/ledger` (detallado):** el ledger detallado devuelve una fila "
        "por `ledger_entry` (hasta 2 filas por transacción de cambio). Esta vista las "
        "colapsa en una sola fila con columnas `egreso_mxn`, `egreso_gtq`, `ingreso_mxn`, "
        "`ingreso_gtq`.\n\n"
        "**Convención egreso / ingreso (perspectiva empresa):**\n"
        "- `egreso` = CREDIT en ledger (empresa dio al cliente)\n"
        "- `ingreso` = DEBIT en ledger (empresa recibió del cliente)\n\n"
        "**Posición neta en `summary`:**\n"
        "- `net_mxn = total_ingreso_mxn - total_egreso_mxn`\n"
        "- `net_gtq = total_ingreso_gtq - total_egreso_gtq`\n"
        "- `net > 0` → `CLIENT_OWES` (el cliente nos debe)\n"
        "- `net < 0` → `COMPANY_OWES` (le debemos al cliente)\n"
        "- `net = 0` → `SETTLED`\n\n"
        "El `summary` siempre refleja el rango completo de fechas, "
        "independiente de la paginación. Solo transacciones `ACTIVE`."
    ),
)
def get_ledger_summary(
    client_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    date_from: Optional[datetime.date] = Query(None, description="Desde fecha (YYYY-MM-DD)"),
    date_to: Optional[datetime.date] = Query(None, description="Hasta fecha (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if date_from and date_to and date_to < date_from:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="date_to debe ser mayor o igual a date_from",
        )
    ClientService(db).get_or_404(client_id)
    return LedgerService(db).get_grouped_ledger(
        client_id,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit,
    )

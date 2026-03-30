from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.schemas.ledger import BalanceOut, LedgerResponse
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
)
def get_balance(
    client_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    ClientService(db).get_or_404(client_id)  # valida existencia
    return LedgerService(db).get_balance(client_id)


@router.get(
    "/{client_id}/ledger",
    response_model=LedgerResponse,
    summary="Libro mayor del cliente",
)
def get_ledger(
    client_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    ClientService(db).get_or_404(client_id)  # valida existencia
    return LedgerService(db).get_ledger(client_id, skip=skip, limit=limit)

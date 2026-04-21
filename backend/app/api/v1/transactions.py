import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.transaction import TransactionType
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionOut, VoidRequest
from app.services.auth_service import get_current_user
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=List[TransactionOut], summary="Listar transacciones")
def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    status: Optional[str] = Query(None, description="Filtrar por estado: ACTIVE o VOIDED"),
    client_id: Optional[UUID] = Query(None, description="Filtrar por cliente"),
    transaction_type: Optional[TransactionType] = Query(
        None,
        description="Filtrar por tipo: SELL_MXN, BUY_MXN, SELL_GTQ, BUY_GTQ, PAYMENT, WITHDRAWAL",
    ),
    date_from: Optional[datetime.date] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    date_to: Optional[datetime.date] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return TransactionService(db).list(
        skip=skip,
        limit=limit,
        status_filter=status,
        client_id=client_id,
        transaction_type=transaction_type,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{txn_id}", response_model=TransactionOut, summary="Obtener transacción por ID")
def get_transaction(
    txn_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    svc = TransactionService(db)
    txn = svc.repo.get_by_id(txn_id)
    if not txn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transacción {txn_id} no encontrada",
        )
    return TransactionOut.model_validate(txn)


@router.post("", response_model=TransactionOut, status_code=201, summary="Registrar transacción")
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService(db).create(payload, current_user)


@router.post(
    "/{txn_id}/void",
    response_model=TransactionOut,
    summary="Anular transacción",
)
def void_transaction(
    txn_id: UUID,
    payload: VoidRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService(db).void(txn_id, payload, current_user)

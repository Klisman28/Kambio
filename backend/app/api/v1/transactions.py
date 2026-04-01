from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
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
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return TransactionService(db).list(skip=skip, limit=limit, status=status)


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

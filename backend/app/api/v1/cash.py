from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.cash import CashCloseRequest, CashOpenRequest, CashSessionOut
from app.services.auth_service import get_current_user
from app.services.cash_service import CashService

router = APIRouter(prefix="/cash", tags=["cash"])


@router.get("/current", response_model=CashSessionOut, summary="Caja actualmente abierta")
def get_current_cash(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return CashService(db).get_current()


@router.post("/open", response_model=CashSessionOut, status_code=201, summary="Abrir caja")
def open_cash(
    payload: CashOpenRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CashService(db).open(payload, current_user)


@router.post("/{session_id}/close", response_model=CashSessionOut, summary="Cerrar caja")
def close_cash(
    session_id: UUID,
    payload: CashCloseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CashService(db).close(session_id, payload, current_user)

from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/ledger", tags=["ledger"])


@router.get("/{client_id}", summary="Libro mayor del cliente [Fase 1]")
def get_ledger(client_id: str, _=Depends(get_current_user)):
    # TODO Fase 1
    return {"detail": "not implemented yet"}


@router.get("/{client_id}/balance", summary="Saldo del cliente [Fase 1]")
def get_balance(client_id: str, _=Depends(get_current_user)):
    # TODO Fase 1
    return {"detail": "not implemented yet"}

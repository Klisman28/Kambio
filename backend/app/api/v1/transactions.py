from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", summary="Listar transacciones [Fase 1]")
def list_transactions(_=Depends(get_current_user)):
    # TODO Fase 1
    return {"detail": "not implemented yet"}


@router.post("", summary="Registrar transacción [Fase 1]")
def create_transaction(_=Depends(get_current_user)):
    # TODO Fase 1
    return {"detail": "not implemented yet"}

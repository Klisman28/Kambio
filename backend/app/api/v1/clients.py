from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", summary="Listar clientes [Fase 1]")
def list_clients(_=Depends(get_current_user)):
    # TODO Fase 1
    return {"detail": "not implemented yet"}


@router.post("", summary="Crear cliente [Fase 1]")
def create_client(_=Depends(get_current_user)):
    # TODO Fase 1
    return {"detail": "not implemented yet"}

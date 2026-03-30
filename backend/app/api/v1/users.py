from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", summary="Listar usuarios [Fase 1]")
def list_users(_=Depends(require_role("admin"))):
    # TODO Fase 1: implementar listado de usuarios
    return {"detail": "not implemented yet"}


@router.post("", summary="Crear usuario [Fase 1]")
def create_user(_=Depends(require_role("admin"))):
    # TODO Fase 1
    return {"detail": "not implemented yet"}

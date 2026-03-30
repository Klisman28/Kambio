from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/cash", tags=["cash"])


@router.get("/current", summary="Estado actual de la caja [Fase 2]")
def get_current_cash(_=Depends(get_current_user)):
    # TODO Fase 2
    return {"detail": "not implemented yet"}


@router.post("/open", summary="Abrir caja [Fase 2]")
def open_cash(_=Depends(get_current_user)):
    # TODO Fase 2
    return {"detail": "not implemented yet"}


@router.post("/close", summary="Cerrar caja [Fase 2]")
def close_cash(_=Depends(get_current_user)):
    # TODO Fase 2
    return {"detail": "not implemented yet"}

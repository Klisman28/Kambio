from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/transactions", summary="Reporte de transacciones [Fase 2]")
def report_transactions(_=Depends(get_current_user)):
    # TODO Fase 2
    return {"detail": "not implemented yet"}


@router.get("/cash-summary", summary="Resumen de cajas [Fase 2]")
def report_cash_summary(_=Depends(get_current_user)):
    # TODO Fase 2
    return {"detail": "not implemented yet"}

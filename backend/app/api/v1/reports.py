import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.report import CashReport, TransactionAnalytics, TransactionReport
from app.services.auth_service import get_current_user
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/transactions", response_model=TransactionReport, summary="Reporte de transacciones detallado")
def report_transactions(
    start_date: datetime.date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: datetime.date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    # Convert dates to datetime using min/max times for inclusive range
    start_dt = datetime.datetime.combine(start_date, datetime.time.min).replace(tzinfo=datetime.timezone.utc)
    end_dt = datetime.datetime.combine(end_date, datetime.time.max).replace(tzinfo=datetime.timezone.utc)
    
    return ReportService(db).get_transaction_report(start_dt, end_dt)


@router.get(
    "/transactions/analytics",
    response_model=TransactionAnalytics,
    summary="Analytics de transacciones — series diarias + distribución por tipo",
    description=(
        "Devuelve datos pre-agregados para gráficas: "
        "una serie diaria (count, MXN, GTQ, comisión por día) "
        "y distribución por tipo de transacción. "
        "Solo transacciones ACTIVE. Sin paginación."
    ),
)
def transaction_analytics(
    start_date: datetime.date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: datetime.date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_date debe ser mayor o igual a start_date",
        )
    start_dt = datetime.datetime.combine(start_date, datetime.time.min).replace(tzinfo=datetime.timezone.utc)
    end_dt = datetime.datetime.combine(end_date, datetime.time.max).replace(tzinfo=datetime.timezone.utc)
    return ReportService(db).get_transaction_analytics(start_dt, end_dt)


@router.get("/cash-summary", response_model=CashReport, summary="Resumen de cortes de caja")
def report_cash_summary(
    start_date: datetime.date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: datetime.date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    start_dt = datetime.datetime.combine(start_date, datetime.time.min).replace(tzinfo=datetime.timezone.utc)
    end_dt = datetime.datetime.combine(end_date, datetime.time.max).replace(tzinfo=datetime.timezone.utc)
    
    return ReportService(db).get_cash_summary_report(start_dt, end_dt)

import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.report import CashReport, TransactionReport
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

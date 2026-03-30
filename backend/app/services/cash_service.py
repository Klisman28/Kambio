from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cash_session import CashSession, CashStatus
from app.models.user import User
from app.repositories.cash_repo import CashRepository
from app.schemas.cash import CashCloseRequest, CashOpenRequest
from app.services.audit_service import AuditService


class CashService:
    def __init__(self, db: Session):
        self.repo = CashRepository(db)
        self.audit = AuditService(db)
        self.db = db

    def get_current(self) -> CashSession:
        session = self.repo.get_open()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay caja abierta",
            )
        return session

    def open(self, payload: CashOpenRequest, current_user: User) -> CashSession:
        existing = self.repo.get_open()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una caja abierta. Ciérrala antes de abrir una nueva.",
            )

        cash = CashSession(
            opening_amount_mxn=payload.opening_amount_mxn,
            opening_amount_gtq=payload.opening_amount_gtq,
            notes=payload.notes,
            opened_by=current_user.id,
        )
        self.repo.create(cash)
        self.audit.log(
            action="cash.open",
            resource_type="cash_session",
            resource_id=cash.id,
            user_id=current_user.id,
            payload={
                "opening_amount_mxn": str(payload.opening_amount_mxn),
                "opening_amount_gtq": str(payload.opening_amount_gtq),
            },
        )
        self.db.commit()
        self.db.refresh(cash)
        return cash

    def close(
        self,
        session_id: UUID,
        payload: CashCloseRequest,
        current_user: User,
    ) -> CashSession:
        cash = self.repo.get_by_id(session_id)
        if not cash:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caja no encontrada")
        if cash.status != CashStatus.open:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La caja ya está cerrada",
            )

        # Solo admin puede cerrar caja de otro usuario
        if str(cash.opened_by) != str(current_user.id) and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el admin puede cerrar cajas de otro operador",
            )

        cash.status = CashStatus.closed
        cash.closing_amount_mxn = payload.closing_amount_mxn
        cash.closing_amount_gtq = payload.closing_amount_gtq
        cash.difference_mxn = payload.closing_amount_mxn - cash.opening_amount_mxn
        cash.difference_gtq = payload.closing_amount_gtq - cash.opening_amount_gtq
        cash.closed_by = current_user.id
        if payload.notes:
            cash.notes = payload.notes

        from datetime import datetime
        cash.closed_at = datetime.utcnow()

        self.repo.update(cash)
        self.audit.log(
            action="cash.close",
            resource_type="cash_session",
            resource_id=cash.id,
            user_id=current_user.id,
            payload={
                "closing_amount_mxn": str(payload.closing_amount_mxn),
                "closing_amount_gtq": str(payload.closing_amount_gtq),
                "difference_mxn": str(cash.difference_mxn),
                "difference_gtq": str(cash.difference_gtq),
            },
        )
        self.db.commit()
        self.db.refresh(cash)
        return cash

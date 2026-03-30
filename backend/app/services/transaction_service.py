from datetime import date, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionStatus
from app.models.user import User
from app.repositories.cash_repo import CashRepository
from app.repositories.client_repo import ClientRepository
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction import TransactionCreate, VoidRequest
from app.services.audit_service import AuditService
from app.services.ledger_service import LedgerService


class TransactionService:
    def __init__(self, db: Session):
        self.repo = TransactionRepository(db)
        self.client_repo = ClientRepository(db)
        self.cash_repo = CashRepository(db)
        self.ledger_svc = LedgerService(db)
        self.audit = AuditService(db)
        self.db = db

    def create(self, payload: TransactionCreate, current_user: User) -> Transaction:
        # 1. Verificar caja abierta
        cash = self.cash_repo.get_open()
        if not cash:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No hay caja abierta. Abre una caja antes de registrar transacciones.",
            )

        # 2. Verificar cliente activo
        client = self.client_repo.get_by_id(payload.client_id)
        if not client or not client.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado o inactivo",
            )

        # 3. Generar código único
        code = self._generate_code()

        # 4. Crear registro de transacción
        txn = Transaction(
            code=code,
            client_id=payload.client_id,
            cash_session_id=cash.id,
            transaction_type=payload.transaction_type,
            amount_mxn=payload.amount_mxn,
            amount_gtq=payload.amount_gtq,
            commission=payload.commission,
            exchange_rate=payload.exchange_rate,
            notes=payload.notes,
            created_by=current_user.id,
        )
        self.repo.create(txn)  # flush — obtiene txn.id sin commit

        # 5. Generar ledger entries (usa estado DB pre-commit para balance_after)
        entries = self.ledger_svc.build_entries_for_transaction(txn)
        for entry in entries:
            self.db.add(entry)

        # 6. Registrar auditoría
        self.audit.log(
            action="transaction.create",
            resource_type="transaction",
            resource_id=txn.id,
            user_id=current_user.id,
            payload={
                "code": code,
                "type": txn.transaction_type,
                "amount_mxn": str(txn.amount_mxn),
                "amount_gtq": str(txn.amount_gtq),
                "commission": str(txn.commission),
                "client_id": str(txn.client_id),
                "cash_session_id": str(txn.cash_session_id),
            },
        )

        # 7. Commit único — ACID
        self.db.commit()
        self.db.refresh(txn)
        return txn

    def void(self, txn_id: UUID, payload: VoidRequest, current_user: User) -> Transaction:
        txn = self.repo.get_by_id(txn_id)
        if not txn:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transacción no encontrada")
        if txn.status != TransactionStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se pueden anular transacciones activas",
            )

        txn.status = TransactionStatus.VOIDED
        txn.voided_by = current_user.id
        txn.voided_at = datetime.utcnow()
        txn.void_reason = payload.void_reason

        self.repo.update(txn)
        self.audit.log(
            action="transaction.void",
            resource_type="transaction",
            resource_id=txn.id,
            user_id=current_user.id,
            payload={
                "code": txn.code,
                "void_reason": payload.void_reason,
                "original_type": txn.transaction_type,
                "amount_mxn": str(txn.amount_mxn),
                "amount_gtq": str(txn.amount_gtq),
            },
        )

        self.db.commit()
        self.db.refresh(txn)
        return txn

    def _generate_code(self) -> str:
        today = date.today().strftime("%Y%m%d")
        count = self.repo.count_all()
        return f"TXN-{today}-{count + 1:05d}"

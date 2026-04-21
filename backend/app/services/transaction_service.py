from datetime import date, datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionStatus
from app.models.user import User
from app.repositories.cash_repo import CashRepository
from app.repositories.client_repo import ClientRepository
from app.repositories.transaction_repo import TransactionRepository
from app.models.transaction import TransactionType
from app.schemas.transaction import TransactionCreate, TransactionOut, VoidRequest
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

    def list(
        self,
        skip: int = 0,
        limit: int = 50,
        status_filter: str | None = None,
        client_id: UUID | None = None,
        transaction_type: TransactionType | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[TransactionOut]:
        rows = self.repo.list_all(
            skip=skip,
            limit=limit,
            status_filter=status_filter,
            client_id=client_id,
            transaction_type=transaction_type,
            date_from=date_from,
            date_to=date_to,
        )
        result = []
        for row in rows:
            out = TransactionOut.model_validate(row.transaction)
            out.client_name = row.client_name
            result.append(out)
        return result

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

        # 5b. Actualizar saldo corriente de caja
        # La caja refleja el efecto INVERSO al ledger del cliente:
        #   - Lo que el cliente recibe (+CREDIT) sale de caja (-)
        #   - Lo que el cliente entrega (-DEBIT) entra a caja (+)
        self._update_cash_balance(cash, txn)

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
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            if "ix_transactions_code" in str(e.orig) or "Duplicate entry" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Colisión de código de transacción. Reintenta la operación.",
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al guardar la transacción.",
            )
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
        # Usar UTC para que coincida con created_at guardado via datetime.utcnow()
        today_utc = datetime.now(timezone.utc).date()
        today_str = today_utc.strftime("%Y%m%d")
        daily_count = self.repo.count_by_date(today_utc)
        return f"TXN-{today_str}-{daily_count + 1:05d}"

    def _update_cash_balance(self, cash, txn: Transaction) -> None:
        """
        Actualiza el saldo corriente de la caja según el tipo de transacción.
        Espejo inverso del ledger del cliente:
          - Lo que el cliente recibe → sale de caja
          - Lo que el cliente entrega → entra a caja
        """
        t = txn.transaction_type

        if t == TransactionType.SELL_MXN:
            # Vendemos MXN al cliente: MXN sale, GTQ entra
            cash.current_amount_mxn -= txn.amount_mxn
            cash.current_amount_gtq += txn.amount_gtq

        elif t == TransactionType.BUY_MXN:
            # Compramos MXN del cliente: MXN entra, GTQ sale
            cash.current_amount_mxn += txn.amount_mxn
            cash.current_amount_gtq -= txn.amount_gtq

        elif t == TransactionType.SELL_GTQ:
            # Vendemos GTQ al cliente: GTQ sale, MXN entra
            cash.current_amount_gtq -= txn.amount_gtq
            cash.current_amount_mxn += txn.amount_mxn

        elif t == TransactionType.BUY_GTQ:
            # Compramos GTQ del cliente: GTQ entra, MXN sale
            cash.current_amount_gtq += txn.amount_gtq
            cash.current_amount_mxn -= txn.amount_mxn

        elif t == TransactionType.PAYMENT:
            # Abono: cliente paga → dinero entra a caja
            if txn.amount_mxn > 0:
                cash.current_amount_mxn += txn.amount_mxn
            if txn.amount_gtq > 0:
                cash.current_amount_gtq += txn.amount_gtq

        elif t == TransactionType.WITHDRAWAL:
            # Retiro: cliente retira → dinero sale de caja
            if txn.amount_mxn > 0:
                cash.current_amount_mxn -= txn.amount_mxn
            if txn.amount_gtq > 0:
                cash.current_amount_gtq -= txn.amount_gtq

        # Sumar comisión a caja (la comisión siempre es ingreso para la empresa)
        if txn.commission and txn.commission > 0:
            # Comisión se cobra en la divisa que el cliente entrega
            if t in (TransactionType.SELL_MXN, TransactionType.SELL_GTQ):
                # El cliente entrega GTQ (SELL_MXN) o MXN (SELL_GTQ)
                pass  # ya está incluida en amount
            elif t in (TransactionType.BUY_MXN, TransactionType.BUY_GTQ):
                pass  # ya está incluida en amount

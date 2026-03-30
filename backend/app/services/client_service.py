from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.user import User
from app.repositories.client_repo import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate
from app.services.audit_service import AuditService


class ClientService:
    def __init__(self, db: Session):
        self.repo = ClientRepository(db)
        self.audit = AuditService(db)
        self.db = db

    def create(self, payload: ClientCreate, current_user: User) -> Client:
        count = self.repo.count()
        code = f"KAM-{count + 1:06d}"

        client = Client(
            code=code,
            full_name=payload.full_name,
            phone=payload.phone,
            email=payload.email,
            address=payload.address,
            id_type=payload.id_type,
            id_number=payload.id_number,
            notes=payload.notes,
            created_by=current_user.id,
        )
        self.repo.create(client)
        self.audit.log(
            action="client.create",
            resource_type="client",
            resource_id=client.id,
            user_id=current_user.id,
            payload={"code": code, "full_name": payload.full_name},
        )
        self.db.commit()
        self.db.refresh(client)
        return client

    def get_or_404(self, client_id: UUID) -> Client:
        client = self.repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        return client

    def list(self, q: Optional[str] = None, skip: int = 0, limit: int = 50) -> List[Client]:
        if q:
            return self.repo.search(q, skip=skip, limit=limit)
        return self.repo.list_active(skip=skip, limit=limit)

    def update(self, client_id: UUID, payload: ClientUpdate, current_user: User) -> Client:
        client = self.get_or_404(client_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(client, field, value)
        self.repo.update(client)
        self.audit.log(
            action="client.update",
            resource_type="client",
            resource_id=client.id,
            user_id=current_user.id,
            payload=payload.model_dump(exclude_unset=True),
        )
        self.db.commit()
        self.db.refresh(client)
        return client

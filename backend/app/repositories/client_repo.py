from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.models.client import Client


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, client_id: UUID) -> Optional[Client]:
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_by_code(self, code: str) -> Optional[Client]:
        return self.db.query(Client).filter(Client.code == code).first()

    def list_active(self, skip: int = 0, limit: int = 50) -> List[Client]:
        return (
            self.db.query(Client)
            .filter(Client.is_active == True)
            .order_by(Client.full_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(self, q: str, skip: int = 0, limit: int = 50) -> List[Client]:
        pattern = f"%{q}%"
        return (
            self.db.query(Client)
            .filter(
                Client.is_active == True,
                Client.full_name.ilike(pattern),
            )
            .order_by(Client.full_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        return self.db.query(func.count(Client.id)).scalar() or 0

    def create(self, client: Client) -> Client:
        self.db.add(client)
        self.db.flush()
        return client

    def update(self, client: Client) -> Client:
        self.db.flush()
        return client

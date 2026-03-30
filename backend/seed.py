"""
Script de semilla para desarrollo local.
Crea el usuario admin inicial si no existe.

Uso:
    python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User
from app.repositories.user_repo import UserRepository


def seed():
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        existing = repo.get_by_email(settings.SEED_ADMIN_EMAIL)
        if existing:
            print(f"[seed] Admin ya existe: {settings.SEED_ADMIN_EMAIL}")
            return

        admin = User(
            email=settings.SEED_ADMIN_EMAIL,
            hashed_password=hash_password(settings.SEED_ADMIN_PASSWORD),
            full_name="Administrador",
            role="admin",
            is_active=True,
        )
        repo.create(admin)
        print(f"[seed] Admin creado: {settings.SEED_ADMIN_EMAIL}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

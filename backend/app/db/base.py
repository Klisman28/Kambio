# Exporta todos los modelos para que Alembic los detecte en autogenerate
from app.db.base_class import Base  # noqa: F401
from app.models.user import User  # noqa: F401

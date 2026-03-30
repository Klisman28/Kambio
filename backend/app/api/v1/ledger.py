# Módulo ledger — rutas migradas a /clients/{id}/ledger y /clients/{id}/balance
# Ver app/api/v1/clients.py para la implementación actual.
#
# Este archivo se mantiene para no romper el import en router.py.
# Puede reutilizarse para rutas adicionales de ledger en fases futuras.

from fastapi import APIRouter

router = APIRouter(prefix="/ledger", tags=["ledger"])

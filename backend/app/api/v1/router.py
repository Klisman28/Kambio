from fastapi import APIRouter

from app.api.v1 import auth, cash, clients, ledger, reports, transactions, users

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(clients.router)
api_router.include_router(transactions.router)
api_router.include_router(ledger.router)
api_router.include_router(cash.router)
api_router.include_router(reports.router)

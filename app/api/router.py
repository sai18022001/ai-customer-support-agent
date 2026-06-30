from fastapi import APIRouter

from app.api import chat, customers, orders, cases, analytics

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(chat.router)
api_router.include_router(customers.router)
api_router.include_router(orders.router)
api_router.include_router(cases.router)
api_router.include_router(analytics.router)

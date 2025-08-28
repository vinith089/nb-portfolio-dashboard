"""
API v1 router configuration
"""
from fastapi import APIRouter

from app.api.api_v1.endpoints import funds, holdings, stock_prices

# Create API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(funds.router, prefix="/funds", tags=["funds"])
api_router.include_router(holdings.router, prefix="/holdings", tags=["holdings"])
api_router.include_router(stock_prices.router, prefix="/stock-prices", tags=["stock-prices"])

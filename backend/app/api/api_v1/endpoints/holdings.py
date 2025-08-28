"""
Holdings API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.holding import (
    Holding,
    HoldingCreate,
    HoldingUpdate,
    HoldingSummary,
    FundHoldingsResponse
)
from app.services.holding_service import HoldingService
from app.services.fund_service import FundService

router = APIRouter()


@router.get("/")
async def list_holdings(
    skip: int = Query(0, ge=0, description="Number of holdings to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of holdings to return"),
    ticker: Optional[str] = Query(None, description="Filter by ticker symbol"),
    fund_id: Optional[int] = Query(None, description="Filter by fund ID"),
    search: Optional[str] = Query(None, description="Search holdings by ticker or company name"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve holdings with optional filtering
    """
    holding_service = HoldingService(db)
    
    if search:
        holdings = await holding_service.search_holdings(search, limit)
    elif ticker:
        holdings = await holding_service.get_holdings_by_ticker(ticker)
    elif fund_id:
        holdings = await holding_service.get_holdings_by_fund(fund_id)
    else:
        holdings = await holding_service.get_holdings(skip=skip, limit=limit)
    
    # Transform to dictionaries with calculated fields
    result = []
    for holding in holdings:
        cost_basis = holding.shares * holding.purchase_price
        result.append({
            "id": holding.id,
            "fund_id": holding.fund_id,
            "ticker": holding.ticker,
            "company_name": holding.company_name,
            "shares": str(holding.shares),
            "purchase_price": str(holding.purchase_price),
            "purchase_date": holding.purchase_date.isoformat(),
            "sector": holding.sector,
            "market_cap": holding.market_cap,
            "created_at": holding.created_at.isoformat(),
            "updated_at": holding.updated_at.isoformat(),
            "cost_basis": str(cost_basis),
            "current_price": None,
            "current_value": str(cost_basis),  # Fallback to cost basis
            "unrealized_gain_loss": "0",
            "unrealized_gain_loss_percent": "0",
            "weight_in_fund": None,
        })
    
    return result


@router.get("/{holding_id}", response_model=Holding)
async def get_holding(
    holding_id: int,
    db: AsyncSession = Depends(get_db)
) -> Holding:
    """
    Retrieve a specific holding by ID
    """
    holding_service = HoldingService(db)
    holding = await holding_service.get_holding_by_id(holding_id)
    
    if not holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Holding with id {holding_id} not found"
        )
    
    return holding


@router.post("/", response_model=Holding, status_code=status.HTTP_201_CREATED)
async def create_holding(
    holding_data: HoldingCreate,
    db: AsyncSession = Depends(get_db)
) -> Holding:
    """
    Create a new holding
    """
    holding_service = HoldingService(db)
    fund_service = FundService(db)
    
    # Check if fund exists
    fund = await fund_service.get_fund_by_id(holding_data.fund_id)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fund with id {holding_data.fund_id} not found"
        )
    
    holding = await holding_service.create_holding(holding_data)
    return holding


@router.put("/{holding_id}", response_model=Holding)
async def update_holding(
    holding_id: int,
    holding_data: HoldingUpdate,
    db: AsyncSession = Depends(get_db)
) -> Holding:
    """
    Update an existing holding
    """
    holding_service = HoldingService(db)
    
    holding = await holding_service.update_holding(holding_id, holding_data)
    if not holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Holding with id {holding_id} not found"
        )
    
    return holding


@router.delete("/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_holding(
    holding_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a holding
    """
    holding_service = HoldingService(db)
    
    success = await holding_service.delete_holding(holding_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Holding with id {holding_id} not found"
        )


@router.get("/fund/{fund_id}/summary")
async def get_fund_holdings_summary(
    fund_id: int,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Get holdings summary for a specific fund
    """
    holding_service = HoldingService(db)
    fund_service = FundService(db)
    
    # Check if fund exists
    fund = await fund_service.get_fund_by_id(fund_id)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with id {fund_id} not found"
        )
    
    summary = await holding_service.get_fund_holdings_summary(fund_id)
    return summary


@router.get("/fund/{fund_id}/sectors")
async def get_fund_sector_breakdown(
    fund_id: int,
    db: AsyncSession = Depends(get_db)
) -> List[dict]:
    """
    Get sector breakdown for fund holdings
    """
    holding_service = HoldingService(db)
    fund_service = FundService(db)
    
    # Check if fund exists
    fund = await fund_service.get_fund_by_id(fund_id)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with id {fund_id} not found"
        )
    
    sectors = await holding_service.get_sector_breakdown(fund_id)
    return sectors


@router.get("/fund/{fund_id}/top", response_model=List[Holding])
async def get_fund_top_holdings(
    fund_id: int,
    limit: int = Query(10, ge=1, le=50, description="Number of top holdings to return"),
    db: AsyncSession = Depends(get_db)
) -> List[Holding]:
    """
    Get top holdings by value for a fund
    """
    holding_service = HoldingService(db)
    fund_service = FundService(db)
    
    # Check if fund exists
    fund = await fund_service.get_fund_by_id(fund_id)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with id {fund_id} not found"
        )
    
    holdings = await holding_service.get_top_holdings(fund_id, limit)
    return holdings
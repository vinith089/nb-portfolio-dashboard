"""
Fund management API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.fund import (
    Fund, 
    FundCreate, 
    FundUpdate, 
    FundSummary, 
    FundPerformanceResponse,
    PeerComparisonResponse
)
from app.services.fund_service import FundService

router = APIRouter()


@router.get("/", response_model=List[Fund])
async def list_funds(
    skip: int = Query(0, ge=0, description="Number of funds to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of funds to return"),
    search: Optional[str] = Query(None, description="Search funds by name or manager"),
    db: AsyncSession = Depends(get_db)
) -> List[Fund]:
    """
    Retrieve all funds with summary information
    """
    fund_service = FundService(db)
    
    if search:
        funds = await fund_service.search_funds(search, limit)
    else:
        funds = await fund_service.get_funds(skip=skip, limit=limit)
    
    return funds


@router.get("/{fund_id}", response_model=Fund)
async def get_fund(
    fund_id: int,
    db: AsyncSession = Depends(get_db)
) -> Fund:
    """
    Retrieve a specific fund by ID with detailed information
    """
    fund_service = FundService(db)
    fund = await fund_service.get_fund_by_id(fund_id)
    
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with id {fund_id} not found"
        )
    
    return fund


@router.post("/", response_model=Fund, status_code=status.HTTP_201_CREATED)
async def create_fund(
    fund_data: FundCreate,
    db: AsyncSession = Depends(get_db)
) -> Fund:
    """
    Create a new fund
    """
    fund_service = FundService(db)
    
    # Check if fund with same name already exists
    existing_fund = await fund_service.get_fund_by_name(fund_data.name)
    if existing_fund:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fund with name '{fund_data.name}' already exists"
        )
    
    fund = await fund_service.create_fund(fund_data)
    return fund


@router.put("/{fund_id}", response_model=Fund)
async def update_fund(
    fund_id: int,
    fund_data: FundUpdate,
    db: AsyncSession = Depends(get_db)
) -> Fund:
    """
    Update an existing fund
    """
    fund_service = FundService(db)
    
    fund = await fund_service.update_fund(fund_id, fund_data)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with id {fund_id} not found"
        )
    
    return fund


@router.delete("/{fund_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fund(
    fund_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a fund
    """
    fund_service = FundService(db)
    
    success = await fund_service.delete_fund(fund_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with id {fund_id} not found"
        )


@router.get("/{fund_id}/performance", response_model=FundPerformanceResponse)
async def get_fund_performance(
    fund_id: int,
    days: int = Query(30, ge=1, le=365, description="Number of days of performance data"),
    db: AsyncSession = Depends(get_db)
) -> FundPerformanceResponse:
    """
    Get fund performance data for specified number of days
    """
    fund_service = FundService(db)
    
    # Check if fund exists
    fund = await fund_service.get_fund_by_id(fund_id)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with id {fund_id} not found"
        )
    
    performance_data = await fund_service.get_fund_performance(fund_id, days)
    return FundPerformanceResponse(
        fund_id=fund_id,
        fund_name=fund["name"],
        performance_data=performance_data,
        period_days=days
    )


@router.get("/{fund_id}/peers", response_model=PeerComparisonResponse)
async def get_fund_peers(
    fund_id: int,
    db: AsyncSession = Depends(get_db)
) -> PeerComparisonResponse:
    """
    Get peer comparison data for a fund
    """
    fund_service = FundService(db)
    
    # Check if fund exists
    fund = await fund_service.get_fund_by_id(fund_id)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with id {fund_id} not found"
        )
    
    peers_data = await fund_service.get_peer_comparison(fund_id)
    return PeerComparisonResponse(
        fund_id=fund_id,
        fund_name=fund["name"],
        fund_strategy=fund["strategy"],
        fund_performance=fund.get("total_return_percent"),
        peers=peers_data
    )


@router.get("/{fund_id}/stats")
async def get_fund_statistics(
    fund_id: int,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Get fund statistics and metrics
    """
    fund_service = FundService(db)
    
    # Check if fund exists
    fund = await fund_service.get_fund_by_id(fund_id)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with id {fund_id} not found"
        )
    
    return await fund_service.get_fund_statistics(fund_id)
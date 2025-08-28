"""
Stock prices API endpoints
"""
from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.stock_price import (
    StockPrice,
    StockPriceCreate,
    StockPriceUpdate,
    StockPriceSummary,
    StockPriceHistory
)
from app.services.stock_price_service import StockPriceService

router = APIRouter()


@router.get("/", response_model=List[StockPrice])
async def list_stock_prices(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    ticker: Optional[str] = Query(None, description="Filter by ticker symbol"),
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering"),
    db: AsyncSession = Depends(get_db)
) -> List[StockPrice]:
    """
    Retrieve stock prices with optional filtering
    """
    stock_service = StockPriceService(db)
    
    if ticker:
        prices = await stock_service.get_stock_prices_by_ticker(
            ticker, start_date, end_date, limit
        )
    else:
        prices = await stock_service.get_stock_prices(skip=skip, limit=limit)
    
    return prices


@router.get("/tickers")
async def get_available_tickers(
    db: AsyncSession = Depends(get_db)
) -> List[str]:
    """
    Get list of all available ticker symbols
    """
    stock_service = StockPriceService(db)
    tickers = await stock_service.get_tickers_list()
    return tickers


@router.get("/{price_id}", response_model=StockPrice)
async def get_stock_price(
    price_id: int,
    db: AsyncSession = Depends(get_db)
) -> StockPrice:
    """
    Retrieve a specific stock price record by ID
    """
    stock_service = StockPriceService(db)
    price = await stock_service.get_stock_price_by_id(price_id)
    
    if not price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock price with id {price_id} not found"
        )
    
    return price


@router.post("/", response_model=StockPrice, status_code=status.HTTP_201_CREATED)
async def create_stock_price(
    price_data: StockPriceCreate,
    db: AsyncSession = Depends(get_db)
) -> StockPrice:
    """
    Create a new stock price record
    """
    stock_service = StockPriceService(db)
    
    # Check if price already exists for this ticker and date
    existing_price = await stock_service.get_stock_prices_by_ticker(
        price_data.ticker, price_data.date, price_data.date, 1
    )
    if existing_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock price for {price_data.ticker} on {price_data.date} already exists"
        )
    
    price = await stock_service.create_stock_price(price_data)
    return price


@router.put("/{price_id}", response_model=StockPrice)
async def update_stock_price(
    price_id: int,
    price_data: StockPriceUpdate,
    db: AsyncSession = Depends(get_db)
) -> StockPrice:
    """
    Update an existing stock price record
    """
    stock_service = StockPriceService(db)
    
    price = await stock_service.update_stock_price(price_id, price_data)
    if not price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock price with id {price_id} not found"
        )
    
    return price


@router.delete("/{price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock_price(
    price_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a stock price record
    """
    stock_service = StockPriceService(db)
    
    success = await stock_service.delete_stock_price(price_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock price with id {price_id} not found"
        )


@router.get("/ticker/{ticker}/latest", response_model=StockPrice)
async def get_latest_stock_price(
    ticker: str,
    db: AsyncSession = Depends(get_db)
) -> StockPrice:
    """
    Get the latest stock price for a ticker
    """
    stock_service = StockPriceService(db)
    price = await stock_service.get_latest_price(ticker)
    
    if not price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No stock price data found for ticker {ticker}"
        )
    
    return price


@router.get("/ticker/{ticker}/history", response_model=StockPriceHistory)
async def get_stock_price_history(
    ticker: str,
    days: int = Query(30, ge=1, le=365, description="Number of days of history to return"),
    db: AsyncSession = Depends(get_db)
) -> StockPriceHistory:
    """
    Get stock price history for a ticker
    """
    stock_service = StockPriceService(db)
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    prices = await stock_service.get_stock_prices_by_ticker(
        ticker, start_date, end_date, days
    )
    
    if not prices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No stock price history found for ticker {ticker}"
        )
    
    return StockPriceHistory(
        ticker=ticker.upper(),
        start_date=start_date,
        end_date=end_date,
        total_records=len(prices),
        prices=prices
    )


@router.get("/ticker/{ticker}/summary")
async def get_stock_price_summary(
    ticker: str,
    days: int = Query(30, ge=1, le=365, description="Number of days for summary calculation"),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Get stock price summary statistics for a ticker
    """
    stock_service = StockPriceService(db)
    summary = await stock_service.get_price_history_summary(ticker, days)
    
    if summary['total_records'] == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No stock price data found for ticker {ticker} in the last {days} days"
        )
    
    return summary


@router.post("/batch/latest")
async def get_batch_latest_prices(
    tickers: List[str],
    db: AsyncSession = Depends(get_db)
) -> List[StockPrice]:
    """
    Get latest prices for multiple tickers
    """
    if not tickers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one ticker must be provided"
        )
    
    if len(tickers) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 tickers allowed per request"
        )
    
    stock_service = StockPriceService(db)
    prices = await stock_service.get_latest_prices(tickers)
    return prices
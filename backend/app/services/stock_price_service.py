"""
Stock price service for database operations
"""
from datetime import date, timedelta
from decimal import Decimal
from typing import List, Optional
from sqlalchemy import select, func, and_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stock_price import StockPrice
from app.schemas.stock_price import StockPriceCreate, StockPriceUpdate


class StockPriceService:
    """Service class for stock price-related operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_stock_prices(self, skip: int = 0, limit: int = 100) -> List[StockPrice]:
        """Get all stock prices with pagination"""
        query = (
            select(StockPrice)
            .offset(skip)
            .limit(limit)
            .order_by(desc(StockPrice.date), StockPrice.ticker)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_stock_price_by_id(self, price_id: int) -> Optional[StockPrice]:
        """Get a specific stock price by ID"""
        query = select(StockPrice).where(StockPrice.id == price_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def get_stock_prices_by_ticker(
        self, 
        ticker: str, 
        start_date: Optional[date] = None, 
        end_date: Optional[date] = None,
        limit: int = 100
    ) -> List[StockPrice]:
        """Get stock prices for a specific ticker with optional date range"""
        query = select(StockPrice).where(StockPrice.ticker == ticker.upper())
        
        if start_date:
            query = query.where(StockPrice.date >= start_date)
        if end_date:
            query = query.where(StockPrice.date <= end_date)
        
        query = query.order_by(desc(StockPrice.date)).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_latest_price(self, ticker: str) -> Optional[StockPrice]:
        """Get the latest price for a ticker"""
        query = (
            select(StockPrice)
            .where(StockPrice.ticker == ticker.upper())
            .order_by(desc(StockPrice.date))
            .limit(1)
        )
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def get_latest_prices(self, tickers: List[str]) -> List[StockPrice]:
        """Get latest prices for multiple tickers"""
        if not tickers:
            return []
        
        # This is a complex query to get latest price for each ticker
        # Using a subquery to get the max date for each ticker
        subquery = (
            select(
                StockPrice.ticker,
                func.max(StockPrice.date).label('max_date')
            )
            .where(StockPrice.ticker.in_([t.upper() for t in tickers]))
            .group_by(StockPrice.ticker)
            .subquery()
        )
        
        query = (
            select(StockPrice)
            .join(
                subquery,
                and_(
                    StockPrice.ticker == subquery.c.ticker,
                    StockPrice.date == subquery.c.max_date
                )
            )
            .order_by(StockPrice.ticker)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_stock_price(self, price_data: StockPriceCreate) -> StockPrice:
        """Create a new stock price record"""
        price_dict = price_data.model_dump()
        price = StockPrice(**price_dict)
        
        self.db.add(price)
        await self.db.commit()
        await self.db.refresh(price)
        return price
    
    async def update_stock_price(self, price_id: int, price_data: StockPriceUpdate) -> Optional[StockPrice]:
        """Update an existing stock price"""
        price = await self.get_stock_price_by_id(price_id)
        if not price:
            return None
        
        update_data = price_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(price, field, value)
        
        await self.db.commit()
        await self.db.refresh(price)
        return price
    
    async def delete_stock_price(self, price_id: int) -> bool:
        """Delete a stock price record"""
        price = await self.get_stock_price_by_id(price_id)
        if not price:
            return False
        
        await self.db.delete(price)
        await self.db.commit()
        return True
    
    async def get_price_history_summary(self, ticker: str, days: int = 30) -> dict:
        """Get price history summary for a ticker"""
        start_date = date.today() - timedelta(days=days)
        
        query = (
            select(
                func.count(StockPrice.id).label('total_records'),
                func.min(StockPrice.close_price).label('min_price'),
                func.max(StockPrice.close_price).label('max_price'),
                func.avg(StockPrice.close_price).label('avg_price'),
                func.sum(StockPrice.volume).label('total_volume')
            )
            .where(
                and_(
                    StockPrice.ticker == ticker.upper(),
                    StockPrice.date >= start_date
                )
            )
        )
        result = await self.db.execute(query)
        row = result.first()
        
        # Get first and last prices for period return calculation
        first_price_query = (
            select(StockPrice.close_price)
            .where(
                and_(
                    StockPrice.ticker == ticker.upper(),
                    StockPrice.date >= start_date
                )
            )
            .order_by(asc(StockPrice.date))
            .limit(1)
        )
        first_price_result = await self.db.execute(first_price_query)
        first_price = first_price_result.scalar()
        
        last_price_query = (
            select(StockPrice.close_price)
            .where(
                and_(
                    StockPrice.ticker == ticker.upper(),
                    StockPrice.date >= start_date
                )
            )
            .order_by(desc(StockPrice.date))
            .limit(1)
        )
        last_price_result = await self.db.execute(last_price_query)
        last_price = last_price_result.scalar()
        
        period_return = None
        if first_price and last_price and first_price != 0:
            period_return = ((last_price - first_price) / first_price) * 100
        
        return {
            'ticker': ticker.upper(),
            'period_days': days,
            'total_records': row.total_records or 0,
            'min_price': row.min_price,
            'max_price': row.max_price,
            'avg_price': row.avg_price,
            'total_volume': row.total_volume or 0,
            'first_price': first_price,
            'last_price': last_price,
            'period_return_percent': period_return
        }
    
    async def get_daily_gainers_losers(self, date_filter: date, limit: int = 10) -> dict:
        """Get top gainers and losers for a specific date"""
        # This would require calculating daily changes
        # For now, return basic structure
        return {
            'date': date_filter,
            'top_gainers': [],
            'top_losers': []
        }
    
    async def get_tickers_list(self) -> List[str]:
        """Get list of all available tickers"""
        query = select(StockPrice.ticker).distinct().order_by(StockPrice.ticker)
        result = await self.db.execute(query)
        return result.scalars().all()
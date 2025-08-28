"""
Holding service for database operations
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional
from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.holding import Holding
from app.models.fund import Fund
from app.models.stock_price import StockPrice
from app.schemas.holding import HoldingCreate, HoldingUpdate


class HoldingService:
    """Service class for holding-related operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_holdings(self, skip: int = 0, limit: int = 100) -> List[Holding]:
        """Get all holdings with pagination"""
        query = (
            select(Holding)
            .offset(skip)
            .limit(limit)
            .order_by(Holding.ticker)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_holding_by_id(self, holding_id: int) -> Optional[Holding]:
        """Get a specific holding by ID"""
        query = select(Holding).where(Holding.id == holding_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def get_holdings_by_fund(self, fund_id: int) -> List[Holding]:
        """Get all holdings for a specific fund"""
        query = (
            select(Holding)
            .where(Holding.fund_id == fund_id)
            .order_by(Holding.ticker)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_holdings_by_ticker(self, ticker: str) -> List[Holding]:
        """Get all holdings for a specific ticker across all funds"""
        query = (
            select(Holding)
            .options(selectinload(Holding.fund))
            .where(Holding.ticker == ticker.upper())
            .order_by(Holding.fund_id)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_holding(self, holding_data: HoldingCreate) -> Holding:
        """Create a new holding"""
        holding_dict = holding_data.model_dump()
        holding = Holding(**holding_dict)
        
        self.db.add(holding)
        await self.db.commit()
        await self.db.refresh(holding)
        return holding
    
    async def update_holding(self, holding_id: int, holding_data: HoldingUpdate) -> Optional[Holding]:
        """Update an existing holding"""
        holding = await self.get_holding_by_id(holding_id)
        if not holding:
            return None
        
        update_data = holding_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(holding, field, value)
        
        await self.db.commit()
        await self.db.refresh(holding)
        return holding
    
    async def delete_holding(self, holding_id: int) -> bool:
        """Delete a holding"""
        holding = await self.get_holding_by_id(holding_id)
        if not holding:
            return False
        
        await self.db.delete(holding)
        await self.db.commit()
        return True
    
    async def get_fund_holdings_summary(self, fund_id: int) -> dict:
        """Get summary statistics for fund holdings"""
        query = (
            select(
                func.count(Holding.id).label('total_holdings'),
                func.sum(Holding.shares * Holding.purchase_price).label('total_cost_basis'),
                func.count(func.distinct(Holding.ticker)).label('unique_tickers'),
                func.count(func.distinct(Holding.sector)).label('unique_sectors')
            )
            .where(Holding.fund_id == fund_id)
        )
        result = await self.db.execute(query)
        row = result.first()
        
        return {
            'fund_id': fund_id,
            'total_holdings': row.total_holdings or 0,
            'total_cost_basis': row.total_cost_basis or Decimal('0.00'),
            'unique_tickers': row.unique_tickers or 0,
            'unique_sectors': row.unique_sectors or 0
        }
    
    async def get_sector_breakdown(self, fund_id: int) -> List[dict]:
        """Get sector breakdown for fund holdings"""
        query = (
            select(
                Holding.sector,
                func.count(Holding.id).label('count'),
                func.sum(Holding.shares * Holding.purchase_price).label('total_value')
            )
            .where(Holding.fund_id == fund_id)
            .group_by(Holding.sector)
            .order_by(desc('total_value'))
        )
        result = await self.db.execute(query)
        
        sectors = []
        for row in result:
            sectors.append({
                'sector': row.sector or 'Unknown',
                'count': row.count,
                'total_value': row.total_value or Decimal('0.00')
            })
        
        return sectors
    
    async def get_top_holdings(self, fund_id: int, limit: int = 10) -> List[Holding]:
        """Get top holdings by value for a fund"""
        query = (
            select(Holding)
            .where(Holding.fund_id == fund_id)
            .order_by(desc(Holding.shares * Holding.purchase_price))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def search_holdings(self, query_str: str, limit: int = 50) -> List[Holding]:
        """Search holdings by ticker or company name"""
        search_pattern = f"%{query_str.upper()}%"
        query = (
            select(Holding)
            .options(selectinload(Holding.fund))
            .where(
                and_(
                    (Holding.ticker.ilike(search_pattern)) |
                    (Holding.company_name.ilike(search_pattern))
                )
            )
            .order_by(Holding.ticker, Holding.fund_id)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
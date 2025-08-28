"""
Fund service layer for database operations
"""
from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from sqlalchemy.orm import selectinload

from app.models.fund import Fund
from app.models.holding import Holding
from app.models.fund_performance import FundPerformance
from app.models.peer_fund import PeerFund
from app.schemas.fund import (
    FundCreate, 
    FundUpdate, 
    FundSummary, 
    FundPerformanceData, 
    PeerComparisonData
)


class FundService:
    """Service class for fund-related database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_funds(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all funds with summary information and latest performance"""
        query = (
            select(Fund)
            .options(selectinload(Fund.holdings))
            .offset(skip)
            .limit(limit)
            .order_by(Fund.name)
        )
        
        result = await self.db.execute(query)
        funds = result.scalars().all()
        
        # Build enriched fund data
        enriched_funds = []
        for fund in funds:
            latest_perf = await self._get_latest_performance(fund.id)
            
            fund_data = {
                "id": fund.id,
                "name": fund.name,
                "strategy": fund.strategy,
                "inception_date": fund.inception_date,
                "total_aum": str(fund.total_aum),
                "manager_name": fund.manager_name,
                "expense_ratio": str(fund.expense_ratio) if fund.expense_ratio else None,
                "description": fund.description,
                "created_at": fund.created_at,
                "updated_at": fund.updated_at,
                "holdings_count": len(fund.holdings) if fund.holdings else 0,
            }
            
            if latest_perf:
                fund_data.update({
                    "total_return_percent": float(latest_perf.total_return) if latest_perf.total_return else 0.0,
                    "daily_return_percent": float(latest_perf.daily_return) if latest_perf.daily_return else 0.0,
                    "current_value": str(latest_perf.assets_under_management) if latest_perf.assets_under_management else str(fund.total_aum),
                })
            else:
                fund_data.update({
                    "total_return_percent": 0.0,
                    "daily_return_percent": 0.0,
                    "current_value": str(fund.total_aum),
                })
            
            enriched_funds.append(fund_data)
        
        return enriched_funds

    async def _get_latest_performance(self, fund_id: int) -> Optional[FundPerformance]:
        """Get the latest performance record for a fund"""
        query = (
            select(FundPerformance)
            .where(FundPerformance.fund_id == fund_id)
            .order_by(desc(FundPerformance.date))
            .limit(1)
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_fund_by_id(self, fund_id: int) -> Optional[dict]:
        """Get fund by ID with all related data and performance"""
        query = (
            select(Fund)
            .options(selectinload(Fund.holdings))
            .where(Fund.id == fund_id)
        )
        
        result = await self.db.execute(query)
        fund = result.scalar_one_or_none()
        
        if not fund:
            return None
        
        # Get latest performance data
        latest_perf = await self._get_latest_performance(fund.id)
        
        # Calculate unrealized gain/loss from holdings
        total_cost_basis = sum(
            float(holding.shares) * float(holding.purchase_price) 
            for holding in fund.holdings
        ) if fund.holdings else 0.0
        
        current_market_value = float(latest_perf.assets_under_management) if latest_perf and latest_perf.assets_under_management else float(fund.total_aum)
        unrealized_gain_loss = current_market_value - total_cost_basis
        unrealized_gain_loss_percent = (unrealized_gain_loss / total_cost_basis * 100) if total_cost_basis > 0 else 0.0
        
        # Build enriched fund data
        fund_data = {
            "id": fund.id,
            "name": fund.name,
            "strategy": fund.strategy,
            "inception_date": fund.inception_date,
            "total_aum": str(fund.total_aum),
            "manager_name": fund.manager_name,
            "expense_ratio": str(fund.expense_ratio) if fund.expense_ratio else None,
            "description": fund.description,
            "created_at": fund.created_at,
            "updated_at": fund.updated_at,
            "holdings_count": len(fund.holdings) if fund.holdings else 0,
            "unrealized_gain_loss": str(unrealized_gain_loss),
            "unrealized_gain_loss_percent": unrealized_gain_loss_percent,
        }
        
        if latest_perf:
            fund_data.update({
                "total_return_percent": float(latest_perf.total_return) if latest_perf.total_return else 0.0,
                "daily_return_percent": float(latest_perf.daily_return) if latest_perf.daily_return else 0.0,
                "current_value": str(latest_perf.assets_under_management) if latest_perf.assets_under_management else str(fund.total_aum),
            })
        else:
            fund_data.update({
                "total_return_percent": 0.0,
                "daily_return_percent": 0.0,
                "current_value": str(fund.total_aum),
            })
        
        return fund_data

    async def get_fund_by_name(self, name: str) -> Optional[Fund]:
        """Get fund by name"""
        query = select(Fund).where(Fund.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_fund(self, fund_data: FundCreate) -> Fund:
        """Create a new fund"""
        db_fund = Fund(
            name=fund_data.name,
            strategy=fund_data.strategy,
            inception_date=fund_data.inception_date,
            total_aum=fund_data.total_aum,
            manager_name=fund_data.manager_name,
            expense_ratio=fund_data.expense_ratio,
            description=fund_data.description
        )
        
        self.db.add(db_fund)
        await self.db.commit()
        await self.db.refresh(db_fund)
        
        return db_fund

    async def update_fund(self, fund_id: int, fund_data: FundUpdate) -> Optional[Fund]:
        """Update an existing fund"""
        query = select(Fund).where(Fund.id == fund_id)
        result = await self.db.execute(query)
        db_fund = result.scalar_one_or_none()
        
        if not db_fund:
            return None
        
        # Update only provided fields
        update_data = fund_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_fund, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_fund)
        
        return db_fund

    async def delete_fund(self, fund_id: int) -> bool:
        """Delete a fund"""
        query = select(Fund).where(Fund.id == fund_id)
        result = await self.db.execute(query)
        db_fund = result.scalar_one_or_none()
        
        if not db_fund:
            return False
        
        await self.db.delete(db_fund)
        await self.db.commit()
        
        return True

    async def get_fund_performance(self, fund_id: int, days: int = 30) -> List[FundPerformanceData]:
        """Get fund performance data for specified number of days (or all available data if none in range)"""
        start_date = date.today() - timedelta(days=days)
        
        query = (
            select(FundPerformance)
            .where(
                and_(
                    FundPerformance.fund_id == fund_id,
                    FundPerformance.date >= start_date
                )
            )
            .order_by(desc(FundPerformance.date))
        )
        
        result = await self.db.execute(query)
        performances = result.scalars().all()
        
        # If no data in the requested range, get all available data for this fund
        if not performances:
            query = (
                select(FundPerformance)
                .where(FundPerformance.fund_id == fund_id)
                .order_by(desc(FundPerformance.date))
                .limit(90)  # Limit to last 90 records
            )
        
        result = await self.db.execute(query)
        performances = result.scalars().all()
        
        return [
            FundPerformanceData(
                date=perf.date,
                nav_price=perf.nav_price,
                total_return=perf.total_return,
                daily_return=perf.daily_return,
                assets_under_management=perf.assets_under_management
            )
            for perf in performances
        ]

    async def get_peer_comparison(self, fund_id: int) -> List[PeerComparisonData]:
        """Get peer comparison data for a fund"""
        # First get the fund to determine its strategy
        fund = await self.get_fund_by_id(fund_id)
        if not fund:
            return []
        
        # Get peer funds (for now, we'll get all peer funds)
        # In a real implementation, we'd match by strategy/category
        query = select(PeerFund).limit(10)
        result = await self.db.execute(query)
        peer_funds = result.scalars().all()
        
        # Add some realistic performance data for demo purposes
        # In a real system, this would come from actual performance calculations
        demo_returns = [8.5, 12.3, -2.1, 15.7, 6.8, 9.2, 4.3, 11.1, -1.5, 7.9]
        
        return [
            PeerComparisonData(
                fund_id=peer.id,
                fund_name=peer.name,
                benchmark_category=peer.benchmark_category,
                total_aum=peer.total_aum,
                expense_ratio=peer.expense_ratio,
                total_return=demo_returns[i % len(demo_returns)]  # Cycle through demo returns
            )
            for i, peer in enumerate(peer_funds)
        ]

    async def get_fund_statistics(self, fund_id: int) -> dict:
        """Get fund statistics and metrics"""
        fund = await self.get_fund_by_id(fund_id)
        if not fund:
            return {}
        
        # Calculate holdings statistics
        holdings_query = (
            select(
                func.count(Holding.id).label('total_holdings'),
                func.sum(Holding.shares * Holding.purchase_price).label('total_cost_basis')
            )
            .where(Holding.fund_id == fund_id)
        )
        
        result = await self.db.execute(holdings_query)
        stats = result.first()
        
        return {
            'fund_id': fund_id,
            'fund_name': fund.name,
            'total_aum': fund.total_aum,
            'holdings_count': stats.total_holdings or 0,
            'total_cost_basis': stats.total_cost_basis or 0,
            'inception_date': fund.inception_date,
            'strategy': fund.strategy,
            'manager_name': fund.manager_name,
            'expense_ratio': fund.expense_ratio
        }

    async def search_funds(self, query: str, limit: int = 10) -> List[Fund]:
        """Search funds by name or manager"""
        search_query = (
            select(Fund)
            .where(
                func.lower(Fund.name).contains(query.lower()) |
                func.lower(Fund.manager_name).contains(query.lower())
            )
            .limit(limit)
        )
        
        result = await self.db.execute(search_query)
        return result.scalars().all()
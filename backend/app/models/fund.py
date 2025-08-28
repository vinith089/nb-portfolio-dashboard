"""
Fund model representing investment funds
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Enum, Date, Numeric, Text, DateTime
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class FundStrategy(str, enum.Enum):
    """Fund investment strategy enumeration"""
    growth = "growth"
    value = "value"
    blend = "blend"
    income = "income"
    sector_specific = "sector_specific"
    international = "international"
    emerging_markets = "emerging_markets"


class Fund(Base):
    """Fund model for investment funds"""
    
    __tablename__ = "funds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    strategy = Column(Enum(FundStrategy, name='fund_strategy'), nullable=False)
    inception_date = Column(Date, nullable=False)
    total_aum = Column(Numeric(15, 2), nullable=False, default=0.00)
    manager_name = Column(String(255), nullable=True)
    expense_ratio = Column(Numeric(5, 4), default=0.0000)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    holdings = relationship("Holding", back_populates="fund", cascade="all, delete-orphan", lazy="selectin")
    performance_records = relationship("FundPerformance", back_populates="fund", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Fund(id={self.id}, name='{self.name}', strategy='{self.strategy}')>"
    
    @property
    def current_value(self) -> Decimal:
        """Calculate current market value from holdings"""
        if not self.holdings:
            return Decimal('0.00')
        
        total_value = Decimal('0.00')
        for holding in self.holdings:
            if holding.current_price:
                total_value += holding.shares * holding.current_price
            else:
                # Fallback to purchase price if no current price
                total_value += holding.shares * holding.purchase_price
        
        return total_value
    
    @property
    def total_cost_basis(self) -> Decimal:
        """Calculate total cost basis from holdings"""
        if not self.holdings:
            return Decimal('0.00')
        
        return sum(holding.shares * holding.purchase_price for holding in self.holdings)
    
    @property
    def unrealized_gain_loss(self) -> Decimal:
        """Calculate unrealized gain/loss"""
        return self.current_value - self.total_cost_basis
    
    @property
    def unrealized_gain_loss_percent(self) -> Decimal:
        """Calculate unrealized gain/loss percentage"""
        if self.total_cost_basis == 0:
            return Decimal('0.00')
        
        return (self.unrealized_gain_loss / self.total_cost_basis) * Decimal('100')
    
    @property
    def holdings_count(self) -> int:
        """Get number of holdings in the fund"""
        return len(self.holdings) if self.holdings else 0
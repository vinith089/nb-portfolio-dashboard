"""
Holding model representing individual stock positions within funds
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, DateTime, BigInteger
from sqlalchemy.orm import relationship

from app.core.database import Base


class Holding(Base):
    """Holding model for individual stock positions"""
    
    __tablename__ = "holdings"
    
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id", ondelete="CASCADE"), nullable=False, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    company_name = Column(String(255), nullable=True)
    shares = Column(Numeric(15, 4), nullable=False)
    purchase_price = Column(Numeric(10, 4), nullable=False)
    purchase_date = Column(Date, nullable=False)
    sector = Column(String(100), nullable=True)
    market_cap = Column(BigInteger, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fund = relationship("Fund", back_populates="holdings")
    
    def __repr__(self):
        return f"<Holding(id={self.id}, ticker='{self.ticker}', shares={self.shares})>"
    
    @property
    def cost_basis(self) -> Decimal:
        """Calculate cost basis (shares * purchase_price)"""
        return self.shares * self.purchase_price
    
    @property
    def current_price(self) -> Decimal:
        """Get current stock price from latest stock_prices record"""
        # This would typically query the stock_prices table
        # For now, return None to indicate no current price available
        # In a full implementation, this would involve a database query
        return None
    
    @property
    def current_value(self) -> Decimal:
        """Calculate current market value"""
        current_price = self.current_price
        if current_price:
            return self.shares * current_price
        return self.cost_basis  # Fallback to cost basis
    
    @property
    def unrealized_gain_loss(self) -> Decimal:
        """Calculate unrealized gain/loss"""
        return self.current_value - self.cost_basis
    
    @property
    def unrealized_gain_loss_percent(self) -> Decimal:
        """Calculate unrealized gain/loss percentage"""
        if self.cost_basis == 0:
            return Decimal('0.00')
        
        return (self.unrealized_gain_loss / self.cost_basis) * Decimal('100')
    
    @property
    def weight_in_fund(self) -> Decimal:
        """Calculate position weight within the fund"""
        if not self.fund or self.fund.total_cost_basis == 0:
            return Decimal('0.00')
        
        return (self.cost_basis / self.fund.total_cost_basis) * Decimal('100')
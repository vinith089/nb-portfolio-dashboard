"""
Fund performance model for historical NAV and performance data
"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric, DateTime, BigInteger, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class FundPerformance(Base):
    """Fund performance model for historical data"""
    
    __tablename__ = "fund_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    nav_price = Column(Numeric(10, 4), nullable=False)
    total_return = Column(Numeric(8, 4), nullable=True)
    daily_return = Column(Numeric(8, 4), nullable=True)
    assets_under_management = Column(Numeric(15, 2), nullable=True)
    shares_outstanding = Column(BigInteger, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    fund = relationship("Fund", back_populates="performance_records")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('fund_id', 'date', name='uq_fund_date'),
        CheckConstraint('nav_price > 0', name='ck_positive_nav'),
        CheckConstraint('assets_under_management >= 0', name='ck_non_negative_aum'),
        CheckConstraint('shares_outstanding >= 0', name='ck_non_negative_shares'),
    )
    
    def __repr__(self):
        return f"<FundPerformance(fund_id={self.fund_id}, date='{self.date}', nav={self.nav_price})>"
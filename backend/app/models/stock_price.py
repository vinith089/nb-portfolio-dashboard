"""
Stock price model for historical and current stock data
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, BigInteger, UniqueConstraint, CheckConstraint

from app.core.database import Base


class StockPrice(Base):
    """Stock price model for market data"""
    
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    open_price = Column(Numeric(10, 4), nullable=False)
    high_price = Column(Numeric(10, 4), nullable=False)
    low_price = Column(Numeric(10, 4), nullable=False)
    close_price = Column(Numeric(10, 4), nullable=False)
    volume = Column(BigInteger, nullable=False)
    adjusted_close = Column(Numeric(10, 4), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('ticker', 'date', name='uq_ticker_date'),
        CheckConstraint('open_price > 0', name='ck_positive_open'),
        CheckConstraint('high_price > 0', name='ck_positive_high'),
        CheckConstraint('low_price > 0', name='ck_positive_low'),
        CheckConstraint('close_price > 0', name='ck_positive_close'),
        CheckConstraint('volume >= 0', name='ck_non_negative_volume'),
        CheckConstraint('low_price <= open_price', name='ck_low_le_open'),
        CheckConstraint('low_price <= close_price', name='ck_low_le_close'),
        CheckConstraint('open_price <= high_price', name='ck_open_le_high'),
        CheckConstraint('close_price <= high_price', name='ck_close_le_high'),
    )
    
    def __repr__(self):
        return f"<StockPrice(ticker='{self.ticker}', date='{self.date}', close={self.close_price})>"
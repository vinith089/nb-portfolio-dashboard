"""
Peer fund model for benchmark and competitor data
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Enum, Numeric, Text, DateTime, Date
import enum

from app.core.database import Base


class PeerCategory(str, enum.Enum):
    """Peer fund benchmark category enumeration"""
    large_cap_growth = "large_cap_growth"
    large_cap_value = "large_cap_value"
    mid_cap_growth = "mid_cap_growth"
    mid_cap_value = "mid_cap_value"
    small_cap_growth = "small_cap_growth"
    small_cap_value = "small_cap_value"
    international_developed = "international_developed"
    emerging_markets = "emerging_markets"
    sector_technology = "sector_technology"
    sector_healthcare = "sector_healthcare"
    sector_financial = "sector_financial"


class PeerFund(Base):
    """Peer fund model for benchmark comparisons"""
    
    __tablename__ = "peer_funds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    benchmark_category = Column(Enum(PeerCategory, name='peer_category'), nullable=False, index=True)
    total_aum = Column(Numeric(15, 2), nullable=True)
    expense_ratio = Column(Numeric(5, 4), nullable=True)
    inception_date = Column(Date, nullable=True)
    manager_company = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PeerFund(id={self.id}, name='{self.name}', category='{self.benchmark_category}')>"
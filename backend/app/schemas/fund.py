"""
Pydantic schemas for fund-related API requests and responses
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, validator

from app.models.fund import FundStrategy


class FundBase(BaseModel):
    """Base fund schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255, description="Fund name")
    strategy: FundStrategy = Field(..., description="Investment strategy")
    inception_date: date = Field(..., description="Fund inception date")
    manager_name: Optional[str] = Field(None, max_length=255, description="Fund manager name")
    expense_ratio: Optional[Decimal] = Field(None, ge=0, le=10, description="Expense ratio as percentage")
    description: Optional[str] = Field(None, description="Fund description")


class FundCreate(FundBase):
    """Schema for creating a new fund"""
    total_aum: Decimal = Field(default=Decimal('0.00'), ge=0, description="Total assets under management")
    
    @validator('inception_date')
    def validate_inception_date(cls, v):
        if v > date.today():
            raise ValueError('Inception date cannot be in the future')
        return v


class FundUpdate(BaseModel):
    """Schema for updating an existing fund"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    strategy: Optional[FundStrategy] = None
    manager_name: Optional[str] = Field(None, max_length=255)
    expense_ratio: Optional[Decimal] = Field(None, ge=0, le=10)
    description: Optional[str] = None
    total_aum: Optional[Decimal] = Field(None, ge=0)


class FundSummary(FundBase):
    """Schema for fund summary information"""
    id: int
    total_aum: Decimal
    created_at: datetime
    holdings_count: int = Field(default=0, description="Number of holdings in fund")
    current_value: Optional[Decimal] = Field(None, description="Current market value")
    total_return_percent: Optional[Decimal] = Field(None, description="Total return percentage")
    daily_return_percent: Optional[Decimal] = Field(None, description="Daily return percentage")
    
    class Config:
        from_attributes = True


class Fund(FundSummary):
    """Complete fund schema with all details"""
    updated_at: datetime
    unrealized_gain_loss: Optional[Decimal] = Field(None, description="Unrealized gain/loss amount")
    unrealized_gain_loss_percent: Optional[Decimal] = Field(None, description="Unrealized gain/loss percentage")


class FundPerformanceData(BaseModel):
    """Schema for fund performance data point"""
    date: date
    nav_price: Decimal = Field(..., gt=0, description="Net Asset Value price")
    total_return: Optional[Decimal] = Field(None, description="Total return percentage")
    daily_return: Optional[Decimal] = Field(None, description="Daily return percentage")
    assets_under_management: Optional[Decimal] = Field(None, ge=0)
    
    class Config:
        from_attributes = True


class FundPerformanceResponse(BaseModel):
    """Schema for fund performance API response"""
    fund_id: int
    fund_name: str
    performance_data: List[FundPerformanceData]
    period_days: int = Field(..., description="Number of days of performance data")
    
    
class PeerComparisonData(BaseModel):
    """Schema for peer fund comparison data"""
    fund_id: int
    fund_name: str
    benchmark_category: str
    total_aum: Optional[Decimal] = None
    expense_ratio: Optional[Decimal] = None
    total_return: Optional[Decimal] = None
    
    class Config:
        from_attributes = True


class PeerComparisonResponse(BaseModel):
    """Schema for peer comparison API response"""
    fund_id: int
    fund_name: str
    fund_strategy: FundStrategy
    fund_performance: Optional[Decimal] = None
    peers: List[PeerComparisonData]
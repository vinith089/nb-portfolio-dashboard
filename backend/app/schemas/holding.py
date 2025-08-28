"""
Pydantic schemas for holding-related API requests and responses
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, validator


class HoldingBase(BaseModel):
    """Base holding schema with common fields"""
    ticker: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    company_name: Optional[str] = Field(None, max_length=255, description="Company name")
    shares: Decimal = Field(..., gt=0, description="Number of shares owned")
    purchase_price: Decimal = Field(..., gt=0, description="Purchase price per share")
    purchase_date: date = Field(..., description="Date of purchase")
    sector: Optional[str] = Field(None, max_length=100, description="Stock sector")
    market_cap: Optional[int] = Field(None, ge=0, description="Market capitalization")
    
    @validator('ticker')
    def validate_ticker(cls, v):
        return v.upper().strip()
    
    @validator('purchase_date')
    def validate_purchase_date(cls, v):
        if v > date.today():
            raise ValueError('Purchase date cannot be in the future')
        return v


class HoldingCreate(HoldingBase):
    """Schema for creating a new holding"""
    fund_id: int = Field(..., gt=0, description="Fund ID that owns this holding")


class HoldingUpdate(BaseModel):
    """Schema for updating an existing holding"""
    company_name: Optional[str] = Field(None, max_length=255)
    shares: Optional[Decimal] = Field(None, gt=0)
    sector: Optional[str] = Field(None, max_length=100)
    market_cap: Optional[int] = Field(None, ge=0)


class Holding(HoldingBase):
    """Complete holding schema with calculated fields"""
    id: int
    fund_id: int
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields (computed as string to match API expectations)
    cost_basis: str = Field(default="0.00", description="Total cost basis (shares * purchase_price)")
    current_price: Optional[str] = Field(None, description="Current stock price")
    current_value: Optional[str] = Field(None, description="Current market value")
    unrealized_gain_loss: Optional[str] = Field(None, description="Unrealized gain/loss amount")
    unrealized_gain_loss_percent: Optional[str] = Field(None, description="Unrealized gain/loss percentage")
    weight_in_fund: Optional[str] = Field(None, description="Position weight within fund as percentage")
    
    class Config:
        from_attributes = True


class HoldingSummary(BaseModel):
    """Summary holding schema for lists"""
    id: int
    ticker: str
    company_name: Optional[str]
    shares: Decimal
    purchase_price: Decimal
    cost_basis: Decimal
    current_price: Optional[Decimal]
    current_value: Optional[Decimal]
    unrealized_gain_loss_percent: Optional[Decimal]
    weight_in_fund: Optional[Decimal]
    sector: Optional[str]
    
    class Config:
        from_attributes = True


class FundHoldingsResponse(BaseModel):
    """Schema for fund holdings API response"""
    fund_id: int
    fund_name: str
    total_holdings: int
    total_cost_basis: Decimal
    total_current_value: Optional[Decimal]
    total_unrealized_gain_loss: Optional[Decimal]
    holdings: list[HoldingSummary]
"""
Pydantic schemas for stock price-related API requests and responses
"""
from datetime import date as DateType, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class StockPriceBase(BaseModel):
    """Base stock price schema with common fields"""
    ticker: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    date: DateType = Field(..., description="Price date")
    open_price: Decimal = Field(..., gt=0, description="Opening price")
    high_price: Decimal = Field(..., gt=0, description="High price")
    low_price: Decimal = Field(..., gt=0, description="Low price")
    close_price: Decimal = Field(..., gt=0, description="Closing price")
    volume: int = Field(..., ge=0, description="Trading volume")
    adjusted_close: Optional[Decimal] = Field(None, gt=0, description="Adjusted closing price")
    
    @validator('ticker')
    def validate_ticker(cls, v):
        return v.upper().strip()
    
    @validator('date')
    def validate_date(cls, v):
        if v > DateType.today():
            raise ValueError('Price date cannot be in the future')
        return v
    
    @validator('high_price')
    def validate_high_price(cls, v, values):
        if 'low_price' in values and v < values['low_price']:
            raise ValueError('High price must be >= low price')
        if 'open_price' in values and v < values['open_price']:
            raise ValueError('High price must be >= open price')
        if 'close_price' in values and v < values['close_price']:
            raise ValueError('High price must be >= close price')
        return v
    
    @validator('low_price')
    def validate_low_price(cls, v, values):
        if 'open_price' in values and v > values['open_price']:
            raise ValueError('Low price must be <= open price')
        if 'close_price' in values and v > values['close_price']:
            raise ValueError('Low price must be <= close price')
        return v


class StockPriceCreate(StockPriceBase):
    """Schema for creating a new stock price record"""
    pass


class StockPriceUpdate(BaseModel):
    """Schema for updating an existing stock price record"""
    open_price: Optional[Decimal] = Field(None, gt=0)
    high_price: Optional[Decimal] = Field(None, gt=0)
    low_price: Optional[Decimal] = Field(None, gt=0)
    close_price: Optional[Decimal] = Field(None, gt=0)
    volume: Optional[int] = Field(None, ge=0)
    adjusted_close: Optional[Decimal] = Field(None, gt=0)


class StockPrice(StockPriceBase):
    """Complete stock price schema with all details"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class StockPriceSummary(BaseModel):
    """Summary stock price information"""
    ticker: str
    date: DateType
    close_price: Decimal
    volume: int
    daily_change: Optional[Decimal] = Field(None, description="Daily price change")
    daily_change_percent: Optional[Decimal] = Field(None, description="Daily percentage change")
    
    class Config:
        from_attributes = True


class StockPriceHistory(BaseModel):
    """Schema for stock price history response"""
    ticker: str
    start_date: DateType
    end_date: DateType
    total_records: int
    prices: List[StockPrice]


class MarketSummary(BaseModel):
    """Schema for market summary data"""
    date: DateType
    total_tickers: int
    avg_volume: int
    top_gainers: List[StockPriceSummary]
    top_losers: List[StockPriceSummary]
"""
Pydantic schemas for stock-related API requests and responses
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class StockPriceBase(BaseModel):
    """Base stock price schema"""
    ticker: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    date: date = Field(..., description="Price date")
    open_price: Decimal = Field(..., gt=0, description="Opening price")
    high_price: Decimal = Field(..., gt=0, description="High price")
    low_price: Decimal = Field(..., gt=0, description="Low price")
    close_price: Decimal = Field(..., gt=0, description="Closing price")
    volume: int = Field(..., ge=0, description="Trading volume")
    adjusted_close: Optional[Decimal] = Field(None, gt=0, description="Adjusted closing price")
    
    @validator('ticker')
    def validate_ticker(cls, v):
        return v.upper().strip()
    
    @validator('high_price')
    def validate_high_price(cls, v, values):
        if 'low_price' in values and v < values['low_price']:
            raise ValueError('High price cannot be less than low price')
        return v
    
    @validator('low_price')
    def validate_low_price(cls, v, values):
        if 'open_price' in values and v > values['open_price']:
            raise ValueError('Low price cannot be greater than open price')
        if 'close_price' in values and v > values['close_price']:
            raise ValueError('Low price cannot be greater than close price')
        return v


class StockPriceCreate(StockPriceBase):
    """Schema for creating stock price data"""
    pass


class StockPriceUpdate(BaseModel):
    """Schema for updating stock price data"""
    open_price: Optional[Decimal] = Field(None, gt=0)
    high_price: Optional[Decimal] = Field(None, gt=0)
    low_price: Optional[Decimal] = Field(None, gt=0)
    close_price: Optional[Decimal] = Field(None, gt=0)
    volume: Optional[int] = Field(None, ge=0)
    adjusted_close: Optional[Decimal] = Field(None, gt=0)


class StockPrice(StockPriceBase):
    """Complete stock price schema"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CurrentStockPrice(BaseModel):
    """Schema for current stock price"""
    ticker: str
    price: Decimal = Field(..., gt=0, description="Current price")
    change: Optional[Decimal] = Field(None, description="Price change from previous close")
    change_percent: Optional[Decimal] = Field(None, description="Percentage change from previous close")
    volume: Optional[int] = Field(None, ge=0, description="Current day volume")
    last_updated: datetime = Field(..., description="Last price update timestamp")
    
    class Config:
        from_attributes = True


class BulkStockPriceRequest(BaseModel):
    """Schema for bulk stock price update request"""
    prices: List[StockPriceCreate] = Field(..., min_items=1, max_items=100)
    
    @validator('prices')
    def validate_unique_ticker_dates(cls, v):
        seen = set()
        for price in v:
            key = (price.ticker, price.date)
            if key in seen:
                raise ValueError(f'Duplicate ticker-date combination: {price.ticker} on {price.date}')
            seen.add(key)
        return v


class BulkStockPriceResponse(BaseModel):
    """Schema for bulk stock price update response"""
    total_requested: int
    successful_updates: int
    failed_updates: int
    errors: List[str] = Field(default_factory=list)


class StockHistoryRequest(BaseModel):
    """Schema for stock price history request"""
    ticker: str = Field(..., min_length=1, max_length=10)
    start_date: Optional[date] = Field(None, description="Start date for history")
    end_date: Optional[date] = Field(None, description="End date for history")
    days: Optional[int] = Field(None, ge=1, le=365, description="Number of days of history")
    
    @validator('ticker')
    def validate_ticker(cls, v):
        return v.upper().strip()
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('End date cannot be before start date')
        return v


class StockHistoryResponse(BaseModel):
    """Schema for stock price history response"""
    ticker: str
    start_date: date
    end_date: date
    total_records: int
    prices: List[StockPrice]
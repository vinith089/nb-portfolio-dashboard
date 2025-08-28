-- Portfolio Monitoring Dashboard Database Schema
-- PostgreSQL Database Schema for Fund Management System

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS fund_performance CASCADE;
DROP TABLE IF EXISTS holdings CASCADE;
DROP TABLE IF EXISTS stock_prices CASCADE;
DROP TABLE IF EXISTS peer_funds CASCADE;
DROP TABLE IF EXISTS funds CASCADE;

-- Create enum types
CREATE TYPE fund_strategy AS ENUM (
    'growth',
    'value',
    'blend',
    'income',
    'sector_specific',
    'international',
    'emerging_markets'
);

CREATE TYPE peer_category AS ENUM (
    'large_cap_growth',
    'large_cap_value',
    'mid_cap_growth',
    'mid_cap_value',
    'small_cap_growth',
    'small_cap_value',
    'international_developed',
    'emerging_markets',
    'sector_technology',
    'sector_healthcare',
    'sector_financial'
);

-- Funds table: Core fund information
CREATE TABLE funds (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    strategy fund_strategy NOT NULL,
    inception_date DATE NOT NULL,
    total_aum DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    manager_name VARCHAR(255),
    expense_ratio DECIMAL(5, 4) DEFAULT 0.0000,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Holdings table: Individual stock positions within funds
CREATE TABLE holdings (
    id SERIAL PRIMARY KEY,
    fund_id INTEGER NOT NULL REFERENCES funds(id) ON DELETE CASCADE,
    ticker VARCHAR(10) NOT NULL,
    company_name VARCHAR(255),
    shares DECIMAL(15, 4) NOT NULL,
    purchase_price DECIMAL(10, 4) NOT NULL,
    purchase_date DATE NOT NULL,
    sector VARCHAR(100),
    market_cap BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT positive_shares CHECK (shares > 0),
    CONSTRAINT positive_price CHECK (purchase_price > 0)
);

-- Stock prices table: Historical and current stock price data
CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open_price DECIMAL(10, 4) NOT NULL,
    high_price DECIMAL(10, 4) NOT NULL,
    low_price DECIMAL(10, 4) NOT NULL,
    close_price DECIMAL(10, 4) NOT NULL,
    volume BIGINT NOT NULL,
    adjusted_close DECIMAL(10, 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ticker, date),
    CONSTRAINT positive_prices CHECK (
        open_price > 0 AND high_price > 0 AND 
        low_price > 0 AND close_price > 0
    ),
    CONSTRAINT valid_price_range CHECK (
        low_price <= open_price AND low_price <= close_price AND
        open_price <= high_price AND close_price <= high_price
    )
);

-- Peer funds table: Benchmark/competitor fund data
CREATE TABLE peer_funds (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    benchmark_category peer_category NOT NULL,
    total_aum DECIMAL(15, 2),
    expense_ratio DECIMAL(5, 4),
    inception_date DATE,
    manager_company VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Fund performance table: Historical NAV and performance metrics
CREATE TABLE fund_performance (
    id SERIAL PRIMARY KEY,
    fund_id INTEGER NOT NULL REFERENCES funds(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    nav_price DECIMAL(10, 4) NOT NULL,
    total_return DECIMAL(8, 4),
    daily_return DECIMAL(8, 4),
    assets_under_management DECIMAL(15, 2),
    shares_outstanding BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(fund_id, date),
    CONSTRAINT positive_nav CHECK (nav_price > 0)
);

-- Indexes for performance optimization
CREATE INDEX idx_holdings_fund_id ON holdings(fund_id);
CREATE INDEX idx_holdings_ticker ON holdings(ticker);
CREATE INDEX idx_stock_prices_ticker ON stock_prices(ticker);
CREATE INDEX idx_stock_prices_date ON stock_prices(date);
CREATE INDEX idx_stock_prices_ticker_date ON stock_prices(ticker, date);
CREATE INDEX idx_fund_performance_fund_id ON fund_performance(fund_id);
CREATE INDEX idx_fund_performance_date ON fund_performance(date);
CREATE INDEX idx_fund_performance_fund_date ON fund_performance(fund_id, date);
CREATE INDEX idx_peer_funds_category ON peer_funds(benchmark_category);

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers
CREATE TRIGGER update_funds_updated_at BEFORE UPDATE ON funds
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_holdings_updated_at BEFORE UPDATE ON holdings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for common queries
CREATE VIEW fund_summary AS
SELECT 
    f.id,
    f.name,
    f.strategy,
    f.inception_date,
    f.total_aum,
    f.manager_name,
    f.expense_ratio,
    COUNT(h.id) as total_holdings,
    COALESCE(SUM(h.shares * sp.close_price), 0) as current_market_value,
    fp.nav_price as latest_nav,
    fp.total_return as latest_total_return
FROM funds f
LEFT JOIN holdings h ON f.id = h.fund_id
LEFT JOIN stock_prices sp ON h.ticker = sp.ticker 
LEFT JOIN LATERAL (
    SELECT nav_price, total_return 
    FROM fund_performance 
    WHERE fund_id = f.id 
    ORDER BY date DESC 
    LIMIT 1
) fp ON true
WHERE sp.date = (SELECT MAX(date) FROM stock_prices WHERE ticker = sp.ticker)
   OR sp.date IS NULL
GROUP BY f.id, f.name, f.strategy, f.inception_date, f.total_aum, 
         f.manager_name, f.expense_ratio, fp.nav_price, fp.total_return;

CREATE VIEW holding_details AS
SELECT 
    h.id,
    h.fund_id,
    f.name as fund_name,
    h.ticker,
    h.company_name,
    h.shares,
    h.purchase_price,
    h.purchase_date,
    h.sector,
    sp.close_price as current_price,
    (h.shares * h.purchase_price) as cost_basis,
    (h.shares * sp.close_price) as current_value,
    ((sp.close_price - h.purchase_price) / h.purchase_price * 100) as percent_return,
    (h.shares * (sp.close_price - h.purchase_price)) as unrealized_gain_loss
FROM holdings h
JOIN funds f ON h.fund_id = f.id
LEFT JOIN stock_prices sp ON h.ticker = sp.ticker 
WHERE sp.date = (SELECT MAX(date) FROM stock_prices WHERE ticker = h.ticker)
   OR sp.date IS NULL;

-- Comments for documentation
COMMENT ON TABLE funds IS 'Core fund information managed by the portfolio manager';
COMMENT ON TABLE holdings IS 'Individual stock positions within each fund';
COMMENT ON TABLE stock_prices IS 'Historical stock price data for all holdings';
COMMENT ON TABLE peer_funds IS 'Benchmark and competitor fund data for comparison';
COMMENT ON TABLE fund_performance IS 'Historical NAV and performance metrics for funds';
COMMENT ON VIEW fund_summary IS 'Summary view with key metrics for all funds';
COMMENT ON VIEW holding_details IS 'Detailed view of holdings with current valuations';
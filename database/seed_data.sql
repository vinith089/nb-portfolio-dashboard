-- Portfolio Monitoring Dashboard - Sample Data
-- Sample data for development and testing

-- Insert sample funds
INSERT INTO funds (name, strategy, inception_date, total_aum, manager_name, expense_ratio, description) VALUES
('Tech Growth Fund', 'growth', '2020-01-15', 250000000.00, 'Sarah Johnson', 0.0075, 'Focused on high-growth technology companies'),
('Value Opportunities Fund', 'value', '2019-03-20', 180000000.00, 'Michael Chen', 0.0065, 'Undervalued companies with strong fundamentals'),
('Healthcare Innovation Fund', 'sector_specific', '2021-06-10', 95000000.00, 'Dr. Emily Rodriguez', 0.0085, 'Healthcare and biotech sector investments'),
('Balanced Growth Fund', 'blend', '2018-09-05', 320000000.00, 'David Thompson', 0.0055, 'Balanced approach to growth and value investing'),
('International Equity Fund', 'international', '2017-11-30', 140000000.00, 'Anna Kowalski', 0.0095, 'Diversified international equity exposure');

-- Insert sample holdings for Tech Growth Fund (fund_id = 1)
INSERT INTO holdings (fund_id, ticker, company_name, shares, purchase_price, purchase_date, sector, market_cap) VALUES
(1, 'AAPL', 'Apple Inc.', 75000.00, 145.50, '2023-01-15', 'Technology', 3000000000000),
(1, 'MSFT', 'Microsoft Corporation', 65000.00, 285.20, '2023-02-01', 'Technology', 2800000000000),
(1, 'GOOGL', 'Alphabet Inc.', 25000.00, 102.75, '2023-02-15', 'Technology', 1600000000000),
(1, 'NVDA', 'NVIDIA Corporation', 45000.00, 220.30, '2023-03-01', 'Technology', 1200000000000),
(1, 'TSLA', 'Tesla Inc.', 30000.00, 185.75, '2023-03-15', 'Consumer Discretionary', 800000000000),
(1, 'META', 'Meta Platforms Inc.', 40000.00, 195.40, '2023-04-01', 'Technology', 750000000000),
(1, 'NFLX', 'Netflix Inc.', 20000.00, 340.80, '2023-04-15', 'Communication Services', 180000000000);

-- Insert sample holdings for Value Opportunities Fund (fund_id = 2)
INSERT INTO holdings (fund_id, ticker, company_name, shares, purchase_price, purchase_date, sector, market_cap) VALUES
(2, 'BRK.B', 'Berkshire Hathaway Inc.', 35000.00, 285.90, '2023-01-20', 'Financial Services', 750000000000),
(2, 'JPM', 'JPMorgan Chase & Co.', 55000.00, 135.25, '2023-02-10', 'Financial Services', 450000000000),
(2, 'JNJ', 'Johnson & Johnson', 60000.00, 162.80, '2023-02-25', 'Healthcare', 420000000000),
(2, 'PG', 'Procter & Gamble Co.', 45000.00, 148.30, '2023-03-10', 'Consumer Staples', 350000000000),
(2, 'KO', 'The Coca-Cola Company', 70000.00, 58.40, '2023-03-25', 'Consumer Staples', 250000000000),
(2, 'WMT', 'Walmart Inc.', 50000.00, 142.70, '2023-04-05', 'Consumer Staples', 400000000000);

-- Insert sample holdings for Healthcare Innovation Fund (fund_id = 3)
INSERT INTO holdings (fund_id, ticker, company_name, shares, purchase_price, purchase_date, sector, market_cap) VALUES
(3, 'UNH', 'UnitedHealth Group Inc.', 25000.00, 485.20, '2023-01-25', 'Healthcare', 450000000000),
(3, 'PFE', 'Pfizer Inc.', 80000.00, 42.15, '2023-02-20', 'Healthcare', 280000000000),
(3, 'ABBV', 'AbbVie Inc.', 35000.00, 138.90, '2023-03-05', 'Healthcare', 270000000000),
(3, 'TMO', 'Thermo Fisher Scientific Inc.', 18000.00, 565.30, '2023-03-20', 'Healthcare', 220000000000),
(3, 'ABT', 'Abbott Laboratories', 50000.00, 108.75, '2023-04-10', 'Healthcare', 190000000000);

-- Insert sample holdings for Balanced Growth Fund (fund_id = 4)
INSERT INTO holdings (fund_id, ticker, company_name, shares, purchase_price, purchase_date, sector, market_cap) VALUES
(4, 'SPY', 'SPDR S&P 500 ETF Trust', 100000.00, 385.20, '2023-01-30', 'ETF', 400000000000),
(4, 'AMZN', 'Amazon.com Inc.', 40000.00, 105.80, '2023-02-15', 'Consumer Discretionary', 1200000000000),
(4, 'V', 'Visa Inc.', 35000.00, 225.40, '2023-03-01', 'Financial Services', 480000000000),
(4, 'HD', 'The Home Depot Inc.', 30000.00, 295.50, '2023-03-15', 'Consumer Discretionary', 300000000000),
(4, 'MA', 'Mastercard Incorporated', 25000.00, 355.70, '2023-04-01', 'Financial Services', 340000000000);

-- Insert sample holdings for International Equity Fund (fund_id = 5)
INSERT INTO holdings (fund_id, ticker, company_name, shares, purchase_price, purchase_date, sector, market_cap) VALUES
(5, 'ASML', 'ASML Holding N.V.', 8000.00, 680.45, '2023-01-10', 'Technology', 280000000000),
(5, 'TSM', 'Taiwan Semiconductor Manufacturing', 60000.00, 95.30, '2023-02-05', 'Technology', 520000000000),
(5, 'NESN', 'Nestle S.A.', 45000.00, 115.80, '2023-02-20', 'Consumer Staples', 320000000000),
(5, 'SAP', 'SAP SE', 20000.00, 125.60, '2023-03-05', 'Technology', 150000000000);

-- Insert sample stock prices (recent data for calculation purposes)
INSERT INTO stock_prices (ticker, date, open_price, high_price, low_price, close_price, volume, adjusted_close) VALUES
-- AAPL recent prices
('AAPL', '2024-01-15', 190.50, 193.75, 189.20, 192.80, 52000000, 192.80),
('AAPL', '2024-01-16', 192.80, 195.20, 191.50, 194.60, 48000000, 194.60),
('AAPL', '2024-01-17', 194.60, 196.80, 193.40, 195.25, 45000000, 195.25),

-- MSFT recent prices
('MSFT', '2024-01-15', 385.20, 388.50, 383.10, 386.75, 35000000, 386.75),
('MSFT', '2024-01-16', 386.75, 390.20, 385.30, 388.90, 32000000, 388.90),
('MSFT', '2024-01-17', 388.90, 391.50, 387.20, 389.40, 30000000, 389.40),

-- GOOGL recent prices
('GOOGL', '2024-01-15', 140.25, 142.80, 139.50, 141.90, 28000000, 141.90),
('GOOGL', '2024-01-16', 141.90, 144.20, 140.80, 143.50, 25000000, 143.50),
('GOOGL', '2024-01-17', 143.50, 145.10, 142.30, 144.75, 27000000, 144.75),

-- NVDA recent prices
('NVDA', '2024-01-15', 520.30, 535.80, 515.20, 532.40, 85000000, 532.40),
('NVDA', '2024-01-16', 532.40, 545.60, 528.90, 540.20, 78000000, 540.20),
('NVDA', '2024-01-17', 540.20, 548.30, 535.70, 542.85, 72000000, 542.85),

-- Add more recent prices for other major holdings
('TSLA', '2024-01-17', 240.50, 245.80, 238.20, 243.60, 95000000, 243.60),
('META', '2024-01-17', 340.20, 345.50, 338.90, 342.75, 42000000, 342.75),
('JPM', '2024-01-17', 165.80, 168.20, 164.50, 167.30, 28000000, 167.30),
('JNJ', '2024-01-17', 158.40, 160.20, 157.80, 159.60, 15000000, 159.60),
('UNH', '2024-01-17', 525.30, 530.80, 523.10, 528.90, 18000000, 528.90),
('AMZN', '2024-01-17', 155.80, 158.40, 154.20, 157.30, 65000000, 157.30);

-- Insert sample peer funds for benchmarking
INSERT INTO peer_funds (name, benchmark_category, total_aum, expense_ratio, inception_date, manager_company, description) VALUES
('Vanguard Growth Index Fund', 'large_cap_growth', 45000000000.00, 0.0014, '1992-11-02', 'Vanguard', 'Index fund tracking large-cap growth stocks'),
('Fidelity Contrafund', 'large_cap_growth', 120000000000.00, 0.0085, '1967-05-17', 'Fidelity', 'Active large-cap growth fund'),
('T. Rowe Price Value Fund', 'large_cap_value', 8500000000.00, 0.0069, '1994-09-30', 'T. Rowe Price', 'Value-oriented large-cap equity fund'),
('Vanguard Health Care Fund', 'sector_healthcare', 15000000000.00, 0.0034, '1984-05-23', 'Vanguard', 'Healthcare sector specialist fund'),
('American Funds Growth Fund', 'large_cap_growth', 25000000000.00, 0.0066, '1973-12-01', 'American Funds', 'Long-term growth focused fund'),
('iShares MSCI EAFE ETF', 'international_developed', 75000000000.00, 0.0032, '1996-08-14', 'BlackRock', 'International developed markets ETF');

-- Insert sample fund performance data
INSERT INTO fund_performance (fund_id, date, nav_price, total_return, daily_return, assets_under_management, shares_outstanding) VALUES
-- Tech Growth Fund performance (fund_id = 1)
(1, '2024-01-15', 125.40, 15.20, 0.85, 255000000.00, 2032000),
(1, '2024-01-16', 126.80, 15.95, 1.12, 257000000.00, 2032000),
(1, '2024-01-17', 127.25, 16.30, 0.35, 258000000.00, 2032000),

-- Value Opportunities Fund performance (fund_id = 2)
(2, '2024-01-15', 98.75, 8.45, 0.42, 182000000.00, 1843000),
(2, '2024-01-16', 99.20, 8.95, 0.46, 183000000.00, 1843000),
(2, '2024-01-17', 99.55, 9.32, 0.35, 183500000.00, 1843000),

-- Healthcare Innovation Fund performance (fund_id = 3)
(3, '2024-01-15', 112.30, 12.80, 0.65, 96500000.00, 859000),
(3, '2024-01-16', 113.10, 13.60, 0.71, 97200000.00, 859000),
(3, '2024-01-17', 113.85, 14.35, 0.66, 97800000.00, 859000),

-- Balanced Growth Fund performance (fund_id = 4)
(4, '2024-01-15', 145.80, 10.25, 0.55, 325000000.00, 2230000),
(4, '2024-01-16', 146.50, 10.75, 0.48, 326500000.00, 2230000),
(4, '2024-01-17', 147.15, 11.20, 0.44, 328000000.00, 2230000),

-- International Equity Fund performance (fund_id = 5)
(5, '2024-01-15', 88.90, 6.75, 0.38, 141500000.00, 1591000),
(5, '2024-01-16', 89.45, 7.35, 0.62, 142300000.00, 1591000),
(5, '2024-01-17', 89.85, 7.82, 0.45, 142900000.00, 1591000);

-- Add historical performance data (last 30 days sample)
INSERT INTO fund_performance (fund_id, date, nav_price, total_return, daily_return, assets_under_management) 
SELECT 
    1, -- Tech Growth Fund
    generate_series(
        '2023-12-18'::date, 
        '2024-01-14'::date, 
        '1 day'::interval
    )::date as date,
    120.00 + (random() * 10 - 5) as nav_price, -- Random price between 115-125
    (random() * 20 - 5) as total_return, -- Random return between -5% to 15%
    (random() * 4 - 2) as daily_return, -- Random daily return between -2% to 2%
    250000000 + (random() * 10000000 - 5000000) as assets_under_management
;
"""
Database seeding functionality for Portfolio Monitoring Dashboard
"""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.models.fund import Fund, FundStrategy
from app.models.holding import Holding
from app.models.stock_price import StockPrice
from app.models.fund_performance import FundPerformance
from app.models.peer_fund import PeerFund, PeerCategory


async def check_if_seeded(db: AsyncSession) -> bool:
    """Check if database already has seed data"""
    result = await db.execute(text("SELECT COUNT(*) FROM funds"))
    count = result.scalar()
    return count > 0


async def seed_database(db: AsyncSession) -> None:
    """Seed the database with sample data"""
    
    # Check if already seeded
    if await check_if_seeded(db):
        print("Database already contains data, skipping seeding...")
        return
    
    print("Seeding database with sample data...")
    
    # Create sample funds
    funds_data = [
        {
            "name": "Tech Growth Fund",
            "strategy": FundStrategy.growth,
            "inception_date": date(2020, 1, 15),
            "total_aum": Decimal("250000000.00"),
            "manager_name": "Sarah Johnson",
            "expense_ratio": Decimal("0.0075"),
            "description": "Focused on high-growth technology companies"
        },
        {
            "name": "Value Opportunities Fund", 
            "strategy": FundStrategy.value,
            "inception_date": date(2019, 3, 20),
            "total_aum": Decimal("180000000.00"),
            "manager_name": "Michael Chen",
            "expense_ratio": Decimal("0.0065"),
            "description": "Undervalued companies with strong fundamentals"
        },
        {
            "name": "Healthcare Innovation Fund",
            "strategy": FundStrategy.sector_specific,
            "inception_date": date(2021, 6, 10),
            "total_aum": Decimal("95000000.00"),
            "manager_name": "Dr. Emily Rodriguez",
            "expense_ratio": Decimal("0.0085"),
            "description": "Healthcare and biotech sector investments"
        },
        {
            "name": "Balanced Growth Fund",
            "strategy": FundStrategy.blend,
            "inception_date": date(2018, 9, 5),
            "total_aum": Decimal("320000000.00"),
            "manager_name": "David Thompson",
            "expense_ratio": Decimal("0.0055"),
            "description": "Balanced approach to growth and value investing"
        },
        {
            "name": "International Equity Fund",
            "strategy": FundStrategy.international,
            "inception_date": date(2017, 11, 30),
            "total_aum": Decimal("140000000.00"),
            "manager_name": "Anna Kowalski",
            "expense_ratio": Decimal("0.0095"),
            "description": "Diversified international equity exposure"
        }
    ]
    
    # Add funds to database
    funds = []
    for fund_data in funds_data:
        fund = Fund(**fund_data)
        db.add(fund)
        funds.append(fund)
    
    await db.flush()  # Get fund IDs
    
    # Create sample holdings for each fund
    holdings_data = [
        # Tech Growth Fund holdings
        {"fund_id": funds[0].id, "ticker": "AAPL", "company_name": "Apple Inc.", "shares": Decimal("75000"), "purchase_price": Decimal("145.50"), "purchase_date": date(2023, 1, 15), "sector": "Technology"},
        {"fund_id": funds[0].id, "ticker": "GOOGL", "company_name": "Alphabet Inc.", "shares": Decimal("35000"), "purchase_price": Decimal("2650.00"), "purchase_date": date(2023, 2, 10), "sector": "Technology"},
        {"fund_id": funds[0].id, "ticker": "MSFT", "company_name": "Microsoft Corporation", "shares": Decimal("45000"), "purchase_price": Decimal("310.20"), "purchase_date": date(2023, 1, 25), "sector": "Technology"},
        {"fund_id": funds[0].id, "ticker": "NVDA", "company_name": "NVIDIA Corporation", "shares": Decimal("25000"), "purchase_price": Decimal("450.75"), "purchase_date": date(2023, 3, 5), "sector": "Technology"},
        {"fund_id": funds[0].id, "ticker": "TSLA", "company_name": "Tesla, Inc.", "shares": Decimal("15000"), "purchase_price": Decimal("875.30"), "purchase_date": date(2023, 2, 20), "sector": "Consumer Discretionary"},
        {"fund_id": funds[0].id, "ticker": "META", "company_name": "Meta Platforms, Inc.", "shares": Decimal("30000"), "purchase_price": Decimal("325.45"), "purchase_date": date(2023, 3, 15), "sector": "Communication Services"},
        {"fund_id": funds[0].id, "ticker": "AMZN", "company_name": "Amazon.com, Inc.", "shares": Decimal("20000"), "purchase_price": Decimal("3100.00"), "purchase_date": date(2023, 1, 30), "sector": "Consumer Discretionary"},
        
        # Value Opportunities Fund holdings
        {"fund_id": funds[1].id, "ticker": "BRK-B", "company_name": "Berkshire Hathaway Inc.", "shares": Decimal("50000"), "purchase_price": Decimal("290.15"), "purchase_date": date(2023, 2, 5), "sector": "Financial Services"},
        {"fund_id": funds[1].id, "ticker": "JPM", "company_name": "JPMorgan Chase & Co.", "shares": Decimal("40000"), "purchase_price": Decimal("135.75"), "purchase_date": date(2023, 1, 20), "sector": "Financial Services"},
        {"fund_id": funds[1].id, "ticker": "JNJ", "company_name": "Johnson & Johnson", "shares": Decimal("35000"), "purchase_price": Decimal("165.25"), "purchase_date": date(2023, 3, 1), "sector": "Healthcare"},
        {"fund_id": funds[1].id, "ticker": "PG", "company_name": "Procter & Gamble Co.", "shares": Decimal("25000"), "purchase_price": Decimal("152.80"), "purchase_date": date(2023, 2, 15), "sector": "Consumer Staples"},
        {"fund_id": funds[1].id, "ticker": "KO", "company_name": "The Coca-Cola Company", "shares": Decimal("60000"), "purchase_price": Decimal("58.45"), "purchase_date": date(2023, 1, 10), "sector": "Consumer Staples"},
        {"fund_id": funds[1].id, "ticker": "WMT", "company_name": "Walmart Inc.", "shares": Decimal("30000"), "purchase_price": Decimal("145.90"), "purchase_date": date(2023, 2, 25), "sector": "Consumer Staples"},
        
        # Healthcare Innovation Fund holdings
        {"fund_id": funds[2].id, "ticker": "UNH", "company_name": "UnitedHealth Group Inc.", "shares": Decimal("15000"), "purchase_price": Decimal("485.20"), "purchase_date": date(2023, 1, 12), "sector": "Healthcare"},
        {"fund_id": funds[2].id, "ticker": "PFE", "company_name": "Pfizer Inc.", "shares": Decimal("80000"), "purchase_price": Decimal("42.15"), "purchase_date": date(2023, 2, 8), "sector": "Healthcare"},
        {"fund_id": funds[2].id, "ticker": "MRNA", "company_name": "Moderna, Inc.", "shares": Decimal("25000"), "purchase_price": Decimal("180.75"), "purchase_date": date(2023, 3, 10), "sector": "Healthcare"},
        {"fund_id": funds[2].id, "ticker": "GILD", "company_name": "Gilead Sciences, Inc.", "shares": Decimal("35000"), "purchase_price": Decimal("78.90"), "purchase_date": date(2023, 1, 25), "sector": "Healthcare"},
        {"fund_id": funds[2].id, "ticker": "BIIB", "company_name": "Biogen Inc.", "shares": Decimal("12000"), "purchase_price": Decimal("275.30"), "purchase_date": date(2023, 2, 18), "sector": "Healthcare"},
        
        # Balanced Growth Fund holdings
        {"fund_id": funds[3].id, "ticker": "SPY", "company_name": "SPDR S&P 500 ETF Trust", "shares": Decimal("100000"), "purchase_price": Decimal("385.75"), "purchase_date": date(2023, 1, 5), "sector": "Diversified"},
        {"fund_id": funds[3].id, "ticker": "QQQ", "company_name": "Invesco QQQ Trust", "shares": Decimal("75000"), "purchase_price": Decimal("315.20"), "purchase_date": date(2023, 1, 15), "sector": "Technology"},
        {"fund_id": funds[3].id, "ticker": "IWM", "company_name": "iShares Russell 2000 ETF", "shares": Decimal("50000"), "purchase_price": Decimal("195.45"), "purchase_date": date(2023, 2, 1), "sector": "Diversified"},
        {"fund_id": funds[3].id, "ticker": "VTI", "company_name": "Vanguard Total Stock Market ETF", "shares": Decimal("60000"), "purchase_price": Decimal("225.80"), "purchase_date": date(2023, 1, 20), "sector": "Diversified"},
        {"fund_id": funds[3].id, "ticker": "GLD", "company_name": "SPDR Gold Shares", "shares": Decimal("40000"), "purchase_price": Decimal("182.15"), "purchase_date": date(2023, 3, 5), "sector": "Commodities"},
        
        # International Equity Fund holdings
        {"fund_id": funds[4].id, "ticker": "VEA", "company_name": "Vanguard FTSE Developed Markets ETF", "shares": Decimal("120000"), "purchase_price": Decimal("45.30"), "purchase_date": date(2023, 1, 8), "sector": "International"},
        {"fund_id": funds[4].id, "ticker": "VWO", "company_name": "Vanguard FTSE Emerging Markets ETF", "shares": Decimal("90000"), "purchase_price": Decimal("38.75"), "purchase_date": date(2023, 2, 12), "sector": "International"},
        {"fund_id": funds[4].id, "ticker": "EFA", "company_name": "iShares MSCI EAFE ETF", "shares": Decimal("80000"), "purchase_price": Decimal("68.90"), "purchase_date": date(2023, 1, 18), "sector": "International"},
        {"fund_id": funds[4].id, "ticker": "FXI", "company_name": "iShares China Large-Cap ETF", "shares": Decimal("60000"), "purchase_price": Decimal("32.45"), "purchase_date": date(2023, 2, 28), "sector": "International"},
    ]
    
    # Add holdings
    for holding_data in holdings_data:
        holding = Holding(**holding_data)
        db.add(holding)
    
    # Add sample peer funds
    peer_funds_data = [
        {"name": "Vanguard Growth Index Fund", "benchmark_category": PeerCategory.large_cap_growth, "total_aum": Decimal("45000000000"), "expense_ratio": Decimal("0.0014"), "manager_company": "Vanguard"},
        {"name": "Fidelity Contrafund", "benchmark_category": PeerCategory.large_cap_growth, "total_aum": Decimal("130000000000"), "expense_ratio": Decimal("0.0085"), "manager_company": "Fidelity"},
        {"name": "T. Rowe Price Blue Chip Growth Fund", "benchmark_category": PeerCategory.large_cap_growth, "total_aum": Decimal("95000000000"), "expense_ratio": Decimal("0.0070"), "manager_company": "T. Rowe Price"},
        {"name": "American Funds Growth Fund of America", "benchmark_category": PeerCategory.large_cap_growth, "total_aum": Decimal("250000000000"), "expense_ratio": Decimal("0.0066"), "manager_company": "American Funds"},
        {"name": "Vanguard Value Index Fund", "benchmark_category": PeerCategory.large_cap_value, "total_aum": Decimal("85000000000"), "expense_ratio": Decimal("0.0014"), "manager_company": "Vanguard"},
        {"name": "Dodge & Cox Stock Fund", "benchmark_category": PeerCategory.large_cap_value, "total_aum": Decimal("75000000000"), "expense_ratio": Decimal("0.0052"), "manager_company": "Dodge & Cox"},
        {"name": "Vanguard Health Care Fund", "benchmark_category": PeerCategory.sector_healthcare, "total_aum": Decimal("15000000000"), "expense_ratio": Decimal("0.0034"), "manager_company": "Vanguard"},
        {"name": "Fidelity Select Health Care Portfolio", "benchmark_category": PeerCategory.sector_healthcare, "total_aum": Decimal("8000000000"), "expense_ratio": Decimal("0.0076"), "manager_company": "Fidelity"},
        {"name": "Vanguard Balanced Index Fund", "benchmark_category": PeerCategory.balanced, "total_aum": Decimal("55000000000"), "expense_ratio": Decimal("0.0015"), "manager_company": "Vanguard"},
        {"name": "American Funds American Balanced Fund", "benchmark_category": PeerCategory.balanced, "total_aum": Decimal("110000000000"), "expense_ratio": Decimal("0.0059"), "manager_company": "American Funds"},
    ]
    
    for peer_data in peer_funds_data:
        peer_fund = PeerFund(**peer_data)
        db.add(peer_fund)
    
    # Commit all changes
    await db.commit()
    print("✅ Database seeded successfully with sample data")
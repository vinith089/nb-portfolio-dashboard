# Prompt 12: Database Auto-Seeding

**User Request:**
```
we need to automatically seed the database with realistic sample data when the FastAPI backend starts up. lets create:

1. 5 different investment funds with various strategies (growth, value, blend, etc.)
2. realistic holdings for each fund (20-30 stocks from actual NYSE companies)
3. historical performance data for charts and analytics
4. peer funds for comparison functionality
5. stock price data for calculations

the seeding should:
- only run if the database is empty
- use realistic financial data (proper AUM amounts, stock tickers, etc.)
- create proper relationships between all entities
- not slow down the startup process
- be idempotent (safe to run multiple times)

lets make it feel like a real portfolio management system with actual fund strategies and holdings.
```

**Context:** User needed realistic sample data to populate the database automatically on startup to make development and testing more realistic and functional.

**Assistant Response:** Implemented comprehensive auto-seeding system with 5 funds with distinct investment strategies, 27 realistic stock holdings across funds, historical fund performance data for 90 days, 10 peer funds for comparison, and startup check to only seed empty database.

**Outcome:** Database automatically populates with realistic financial data on first startup, providing a complete development environment.

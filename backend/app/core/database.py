"""
Database configuration and connection management
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
import asyncpg

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    str(settings.DATABASE_URL),
    poolclass=NullPool,  # Use NullPool for async
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency that provides database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database tables
    """
    async with engine.begin() as conn:
        # Import all models here to ensure they are registered
        from app.models.fund import Fund
        from app.models.holding import Holding
        from app.models.stock_price import StockPrice
        from app.models.peer_fund import PeerFund
        from app.models.fund_performance import FundPerformance
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def check_db_connection() -> bool:
    """
    Check if database connection is working
    """
    try:
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            return result.scalar() == 1
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
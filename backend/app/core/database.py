"""Database configuration and session management."""

import asyncio
from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Database metadata for migrations
metadata = MetaData()

# Base class for ORM models
Base = declarative_base(metadata=metadata)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """Drop all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def check_db_connection() -> bool:
    """Check if database connection is working."""
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False


# For testing
test_engine = None
TestSessionLocal = None

if settings.test_database_url:
    test_engine = create_async_engine(
        settings.test_database_url,
        echo=False,
        pool_pre_ping=True,
    )
    TestSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get test database session."""
    if not TestSessionLocal:
        raise RuntimeError("Test database not configured")
    
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def setup_test_db() -> None:
    """Set up test database."""
    if test_engine:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def teardown_test_db() -> None:
    """Tear down test database."""
    if test_engine:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
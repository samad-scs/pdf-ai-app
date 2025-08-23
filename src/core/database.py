# app/core/database.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.core.config import settings

# --- 1. Async DB URL ---
# Notice the `+asyncpg` part for PostgreSQL async driver
DATABASE_URL = settings.DATABASE_URL

# --- 2. Async Engine ---
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # prints SQL for debugging
    future=True,  # new SQLAlchemy style
)

# --- 3. Async Session Factory ---
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # keeps objects usable after commit
)

# --- 4. Base class for models ---
Base = declarative_base()


# --- 5. Dependency for FastAPI routes ---
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

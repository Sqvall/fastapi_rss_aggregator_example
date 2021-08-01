from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import DB_URL

async_engine = create_async_engine(DB_URL)

async_session = sessionmaker(
    bind=async_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

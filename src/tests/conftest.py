import asyncio
from os import environ

import alembic.config
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

environ['TESTING'] = 'True'  # noqa

from app.db.database import async_session
from app.core import config
from app.main import get_application

assert config.TESTING is True, "TESTING in config.py must be 'True', and appointed before imports from application"


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def apply_migrations() -> None:
    alembic.config.main(argv=["upgrade", "head"])
    yield
    alembic.config.main(argv=["downgrade", "base"])


@pytest.fixture
async def session() -> AsyncSession:
    async with async_session() as session:
        yield session


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return get_application()


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client

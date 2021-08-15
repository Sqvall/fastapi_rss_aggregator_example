import asyncio

import alembic.config
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import async_session


@pytest.yield_fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
def apply_migrations() -> None:
    alembic.config.main(argv=["upgrade", "head"])
    print()
    yield
    print()
    alembic.config.main(argv=["downgrade", "base"])


@pytest.fixture
async def session() -> AsyncSession:
    async with async_session() as session:
        # async with session.begin():
        yield session


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client

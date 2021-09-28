import asyncio
from os import environ

import alembic.config
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.feeds import FeedInCreate

environ['TESTING'] = 'True'  # noqa

from app.db.database import async_session
from app.core import config
from app.main import get_application
from app.models.feeds import Feed
from app.db.repositories.feeds import FeedsRepository

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


@pytest.fixture
async def test_feed(session: AsyncSession) -> Feed:
    feed = FeedInCreate(
        source_url="https://example.com/test_feed",
        name="Test Name",
        can_updated=True
    )

    new_feed = await FeedsRepository(session).create(**feed.dict())
    return new_feed


@pytest.fixture
async def create_50_feeds(session):
    for i in range(1, 51):
        await FeedsRepository(session).create(
            source_url=f'https://example.com/{i}',
            name=f'Some name {i}',
            can_updated=True if i % 2 else False,
        )

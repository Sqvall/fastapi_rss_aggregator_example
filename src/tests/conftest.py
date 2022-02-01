import asyncio
from os import environ
from pathlib import Path

import alembic.config
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_factoryboy import register
from sqlalchemy.ext.asyncio import AsyncSession

environ['TESTING'] = 'True'  # noqa

from services import collector
from db.database import async_session
from core import config
from main import get_application
from models.feeds import Feed
from db.repositories.feeds import FeedsRepository
from schemas.feeds import FeedInCreate
from db.repositories.tags import TagsRepository
from models import Tag
from tests import factories

assert config.TESTING is True, "TESTING in config.py must be 'True', and appointed before imports from src"

register(factories.TagFactory)
register(factories.FeedFactory)
register(factories.EntryBaseFactory)
register(factories.EntryRelatedFactory)


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
    await session.commit()
    return new_feed


@pytest.fixture
async def create_50_feeds(session):
    for i in range(1, 51):
        await FeedsRepository(session).create(
            source_url=f'https://example.com/{i}',
            name=f'Some name {i}',
            can_updated=True if i % 2 else False,
        )
    await session.commit()


@pytest.fixture
async def test_tag(session: AsyncSession) -> Tag:
    new_tag = await TagsRepository(session).create(name='Test tag')
    await session.commit()
    return new_tag


@pytest.fixture(scope='session')
def valid_rss_resp():
    fp = Path(__file__).resolve().parent / 'mock' / 'valid_rss_response.xml'
    result = fp.open().read()
    return result


@pytest.fixture
async def patched_response(valid_rss_resp, monkeypatch):
    async def mocked_fetch_feed_data(*args, **kwargs):
        return valid_rss_resp

    monkeypatch.setattr(collector, 'fetch_feed_data', mocked_fetch_feed_data)

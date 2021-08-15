import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.repositories.feeds import FeedsRepository
from app.schemas.feeds import FeedOut

pytestmark = pytest.mark.asyncio

async def test_empty_feeds_when_on_one_feed(client: AsyncClient):
    response = await client.get("/api/feeds")
    assert response.status_code == 200
    assert response.json() == []


async def test_can_create_feed(app: FastAPI, client: AsyncClient, session: AsyncSession):
    feed_data = {
        "sourceUrl": "https://stackoverflow.com/feeds/tag?tagnames=fastapi&sort=newest",
        "name": "Test Name",
        "canUpdated": True,
    }
    response = await client.post(
        url=app.url_path_for('feeds:create-feed'),
        json=feed_data
    )

    assert response.status_code == status.HTTP_201_CREATED

    created_feed = FeedOut(**response.json())


    feed_from_db = await FeedsRepository(session).get_by_source_url(source_url=created_feed.source_url)

    print(feed_from_db)

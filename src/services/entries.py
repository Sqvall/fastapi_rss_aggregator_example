import logging
from typing import Optional

import feedparser as fp
import httpx
from httpx import Response

from celery_app.tasks import example_task
from db.database import async_session
from db.repositories.entries import EntriesRepository
from db.repositories.feeds import FeedsRepository
from models import Entry
from schemas.feeds import FeedInCreate
from services.errors import CollectFeedDataError

logger = logging.getLogger(__name__)


async def fetch_feed_data(*, client: httpx.AsyncClient, url: str) -> Optional[str]:
    try:
        response = await client.get(url)
    except httpx.RequestError as exc:
        error_message = f"An error occurred while requesting {exc.request.url!r}."
        logger.warning(error_message)
        return None

    return response.text


async def collect_entries_for_feed(*, feed: FeedInCreate):
    example_task.run("hello world")  # TODO Set delay.

    # sqlalchemy.exc.InvalidRequestError:
    # Can't operate on closed transaction inside context manager.
    # Please complete the context manager before emitting further commands.
    async with async_session() as session:
        async with session.begin():
            feed_repo = FeedsRepository(session)

            new_feeds = await feed_repo.create(
                source_url=feed.source_url,
                name=feed.name,
                can_updated=feed.can_updated,
            )

            if not new_feeds.can_updated:
                return

            async with httpx.AsyncClient() as client:
                xml = await fetch_feed_data(client=client, url=feed.source_url)

                if xml is None:
                    return

            parse_data = fp.parse(xml)

            if parse_data.bozo:  # not valid xml or failure response
                error_message = f"Not valid xml or failure response when trying collect entries " \
                                f"for Feed (id: {new_feeds.id})."
                logger.warning(error_message)
                raise CollectFeedDataError(error_message)

            feed_resp = parse_data['channel']

            await FeedsRepository(session).update(
                feed_id=new_feeds.id,
                title=feed_resp.get('title'),
                description=feed_resp.get('subtitle'),
            )

            entries = []

            for i in parse_data['items']:
                entries.append(Entry(link=i['url'], feed_id=new_feeds.id, title=i['title']))

            await EntriesRepository(session).add_all(entries)

            await session.commit()

    return new_feeds

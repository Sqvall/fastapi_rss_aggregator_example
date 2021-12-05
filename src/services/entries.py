import logging
from typing import Optional

import feedparser as fp
import httpx
from httpx import Response

from celery_app.tasks import example_task
from db.database import async_session
from db.repositories.feeds import FeedsRepository
from services.errors import CollectFeedDataError

logger = logging.getLogger(__name__)


async def fetch_feed_data(*, client: httpx.AsyncClient, url: str) -> Optional[Response]:
    try:
        response = await client.get(url)
    except httpx.RequestError as exc:
        error_message = f"An error occurred while requesting {exc.request.url!r}."
        logger.warning(error_message)
        return None

    return response


async def collect_entries_for_feed(*, feed_repo: FeedsRepository, feed_id: int):
    example_task.run("hello world")  # TODO Set delay.

    # sqlalchemy.exc.InvalidRequestError:
    # Can't operate on closed transaction inside context manager.
    # Please complete the context manager before emitting further commands.
    feed = await feed_repo.get_by_id(id_=feed_id)

    async with httpx.AsyncClient() as client:
        result = await fetch_feed_data(client=client, url=feed.source_url)

        if result is None:
            return

    parse_data = fp.parse(result.text)

    if parse_data.bozo:  # not valid xml or failure response
        error_message = f"Not valid xml or failure response when trying collect entries for Feed (id: {feed.id})."
        logger.warning(error_message)
        raise CollectFeedDataError(error_message)

    feed_resp = parse_data['feed']

    await feed_repo.update(
        feed=feed,
        title=feed_resp.get('title'),
        description=feed_resp.get('subtitle'),
    )

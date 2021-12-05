from typing import Optional

import feedparser as fp
import httpx
from httpx import Response

from app.core.celery_app import celery_app
from app.models import Feed


async def fetch_feed_data(*, client: httpx.AsyncClient, url: str) -> Optional[Response]:
    response = None
    try:
        response = await client.get(url)
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    else:
        return response
    return response


async def collect_entries_for_feed(*, feed: Feed):
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])

    async with httpx.AsyncClient() as client:
        result = await fetch_feed_data(client=client, url=feed.source_url)
        print(result)

        if result is None:
            return

    parse_data = fp.parse(result.text)
    #
    # if parse_data.bozo:  # not valid xml or failure response
    #     return

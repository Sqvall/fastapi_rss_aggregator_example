from pydantic import AnyUrl

from models.feeds import Feed


async def feed_create(*, source_url: AnyUrl, name: str, can_updated: bool) -> Feed:
    new_feed = await Feed.create(
        source_url=source_url,
        name=name,
        can_updated=can_updated,
    )
    return new_feed


async def check_feed_exists(*, source_url: AnyUrl, name: str):
    ...
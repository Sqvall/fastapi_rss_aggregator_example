from pydantic import HttpUrl

from db.errors import EntityDoesNotExist
from db.repositories.feeds import FeedsRepository


async def check_feed_with_source_url_exists(feed_repo: FeedsRepository, source_url: HttpUrl) -> bool:
    try:
        await feed_repo.get_by_source_url(source_url=source_url)
    except EntityDoesNotExist:
        return False

    return True

from pydantic import AnyUrl

from app.db.errors import EntityDoesNotExist
from app.db.repositories.feeds import FeedsRepository


async def check_feed_already_exists(feed_repo: FeedsRepository, source_url: AnyUrl) -> bool:
    try:
        await feed_repo.get_by_source_url(source_url)
    except EntityDoesNotExist:
        return False

    return True

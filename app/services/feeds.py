from pydantic import AnyUrl
from sqlalchemy.exc import NoResultFound

from db.repositories.feeds import FeedsRepository


async def check_feed_exists(feed_repo: FeedsRepository, source_url: AnyUrl) -> bool:
    try:
        await feed_repo.get_by_source_url(source_url)
    except NoResultFound:
        return False

    return True

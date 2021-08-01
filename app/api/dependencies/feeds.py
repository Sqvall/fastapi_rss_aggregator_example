from uuid import UUID

from fastapi import Path, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status

from api.dependencies.database import get_repository
from db.repositories.feeds import FeedsRepository
from models.feeds import Feed
from resources import strings


async def get_feed_by_id_from_path(
        feed_id: UUID = Path,
        feeds_repo: FeedsRepository = Depends(get_repository(FeedsRepository)),
) -> Feed:
    try:
        return await feeds_repo.get_by_id(feed_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.FEED_DOES_NOT_EXIST_ERROR,
        )

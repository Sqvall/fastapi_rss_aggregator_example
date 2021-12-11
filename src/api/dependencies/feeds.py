from typing import Optional

from fastapi import Path, Depends, HTTPException, Query
from starlette import status

from api.dependencies.database import get_repository
from db.errors import EntityDoesNotExist
from db.repositories.feeds import FeedsRepository
from models import Feed
from resources import strings


async def get_feed_by_id_from_path(
        feed_id: int = Path,
        feeds_repo: FeedsRepository = Depends(get_repository(FeedsRepository)),
) -> Feed:
    try:
        return await feeds_repo.get_by_id(id_=feed_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.FEED_DOES_NOT_EXIST_ERROR,
        )


async def get_feed_by_id_from_query(
        feed_id: int = Query(None),
        feeds_repo: FeedsRepository = Depends(get_repository(FeedsRepository)),
) -> Optional[Feed]:
    try:
        return await feeds_repo.get_by_id(id_=feed_id)
    except EntityDoesNotExist:
        return None

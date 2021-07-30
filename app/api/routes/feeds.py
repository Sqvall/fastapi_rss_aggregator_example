from fastapi import APIRouter, Body
from starlette import status

from schemas.feeds import FeedOut, FeedIn
from services.feeds import feed_create

router = APIRouter()


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=FeedOut,
    name='feeds:create-feed',
)
async def create_new_feed(feed_in: FeedIn = Body(..., embed=True, alias="feed")) -> FeedOut:

    feed = await feed_create(
        source_url=feed_in.source_url,
        name=feed_in.name,
        can_updated=feed_in.can_updated,
    )

    return FeedOut.from_orm(feed)

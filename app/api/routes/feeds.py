from fastapi import APIRouter
from starlette import status

from models.feeds import Feed
from schemas.feeds import FeedOut, FeedIn

router = APIRouter()


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=FeedOut,
    name='feeds:create-feed',
)
async def create_feed(feed: FeedIn) -> FeedOut:
    new_feed = await Feed.create(**feed.dict(exclude_unset=True))

    return FeedOut.from_orm(new_feed)

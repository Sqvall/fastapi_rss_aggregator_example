from typing import List

from fastapi import APIRouter, Depends, Body, HTTPException
from starlette import status

from app.api.dependencies.database import get_repository
from app.api.dependencies.feeds import get_feed_by_id_from_path
from app.db.repositories.feeds import FeedsRepository
from app.models.feeds import Feed
from app.resources import strings
from app.schemas.feeds import FeedOut, FeedInCreate, FeedInUpdate
from app.services.feeds import check_feed_already_exists

router = APIRouter()


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=FeedOut,
    name='feeds:create-feed',
)
async def create_new_feed(
        feed: FeedInCreate,
        feed_repo: FeedsRepository = Depends(get_repository(FeedsRepository))
):
    if await check_feed_already_exists(feed_repo, feed.source_url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.FEED_WITH_THIS_SOURCE_URL_ALREADY_EXIST.format(feed.source_url)
        )
    new_feeds = await feed_repo.create(
        source_url=feed.source_url,
        name=feed.name,
        can_updated=feed.can_updated,
    )
    return new_feeds


@router.put(
    '/{feed_id}',
    status_code=status.HTTP_200_OK,
    response_model=FeedOut,
    name='feeds:update-feed'
)
async def update_feed(
        feed_updated: FeedInUpdate = Body(..., embed=True, alias='feed'),
        current_feed: Feed = Depends(get_feed_by_id_from_path),
        feed_repo: FeedsRepository = Depends(get_repository(FeedsRepository)),
):
    is_new_source_url = feed_updated.source_url and feed_updated.source_url != current_feed.source_url

    if is_new_source_url:
        if await check_feed_already_exists(feed_repo, feed_updated.source_url):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=strings.FEED_WITH_THIS_SOURCE_URL_ALREADY_EXIST.format(feed_updated.source_url)
            )

    updated_feed = await feed_repo.update(
        feed=current_feed,
        **feed_updated.dict()
    )
    return updated_feed


@router.get(
    '',
    response_model=List[FeedOut],
    name='feeds:list-feeds',
)
async def list_feed(
        feed_repo: FeedsRepository = Depends(get_repository(FeedsRepository))
):
    all_feeds = await feed_repo.get_all_feeds()
    return all_feeds


@router.get(
    '/{feed_id}',
    response_model=FeedOut,
    name="feeds:get-feed",
)
async def retrieve_feed_by_id(
        feed: Feed = Depends(get_feed_by_id_from_path)
):
    return feed

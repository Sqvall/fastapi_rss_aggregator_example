from typing import List, Optional
from uuid import UUID

from pydantic import AnyUrl
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from db.errors import EntityDoesNotExist
from db.repositories.base import BaseRepository
from models.feeds import Feed


class FeedsRepository(BaseRepository):

    async def create(self, *, source_url: AnyUrl, name: str, can_updated: bool) -> Feed:
        new_feed = Feed(
            source_url=str(source_url),
            name=name,
            can_updated=can_updated,
        )
        self.session.add(new_feed)

        await self.session.flush()

        return new_feed

    async def update(
            self,
            *,
            feed: Feed,
            source_url: Optional[str] = None,
            name: Optional[str] = None,
            can_updated: Optional[bool] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
    ):
        feed.source_url = source_url or feed.source_url
        feed.name = name if name is not None else feed.name
        feed.can_updated = can_updated if can_updated is not None else feed.can_updated
        feed.title = title if title is not None else feed.title
        feed.description = description if description is not None else feed.description

        await self.session.commit()

        return feed

    async def get_by_id(self, guid: UUID) -> Feed:
        stmt = select(Feed).where(Feed.guid == guid)
        result = await self.session.execute(stmt)

        try:
            return result.scalars().one()
        except NoResultFound:
            raise EntityDoesNotExist(f'Feed with guid {guid} already exist.')

    async def get_by_source_url(self, source_url: AnyUrl) -> Feed:
        stmt = select(Feed).where(Feed.source_url == source_url)
        result = await self.session.execute(stmt)

        try:
            return result.scalars().one()
        except NoResultFound:
            raise EntityDoesNotExist(f'Feed with source_url {source_url} already exist.')

    async def get_all_feeds(self) -> List[Feed]:
        stmt = select(Feed).order_by(Feed.guid)
        result: Result = await self.session.execute(stmt)

        return result.scalars().all()

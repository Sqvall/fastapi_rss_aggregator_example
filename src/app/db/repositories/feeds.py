import copy
from typing import List, Optional

from sqlalchemy import func, update, insert, delete
from sqlalchemy.engine import ChunkedIteratorResult, CursorResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from app.db.errors import EntityDoesNotExist
from app.db.repositories.base import BaseRepository
from app.models.feeds import Feed


class FeedsRepository(BaseRepository):

    async def create(
            self,
            *,
            source_url: str,
            name: str,
            can_updated: bool
    ) -> Feed:

        new_feed = Feed(
            source_url=source_url,
            name=name,
            can_updated=can_updated,
        )

        self._session.add(new_feed)
        await self._session.commit()

        return new_feed

    async def delete(self, *, feed: Feed):
        stmt = delete(Feed).where(Feed.id == feed.id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def update(
            self,
            *,
            feed: Feed,
            source_url: Optional[str] = None,
            name: Optional[str] = None,
            can_updated: Optional[bool] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
    ) -> Feed:

        feed.source_url = source_url or feed.source_url
        feed.name = name or feed.name
        feed.can_updated = can_updated if can_updated is not None else feed.can_updated
        feed.title = title or feed.title
        feed.description = description or feed.description

        self._session.add(feed)
        await self._session.commit()

        return feed

    async def get_by_id(self, *, id_: int) -> Feed:
        stmt = select(Feed).where(Feed.id == id_)
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise EntityDoesNotExist(f'Feed with id {id_} not exist.')

    async def get_by_source_url(self, *, source_url: str) -> Feed:
        stmt = select(Feed).where(Feed.source_url == source_url)
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise EntityDoesNotExist(f'Feed with source_url {source_url} not exist.')

    async def get_feeds(self, *, limit=20, offset=0) -> List[Feed]:
        stmt = select(Feed).order_by(-Feed.id).offset(offset).limit(limit)
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_total_count(self) -> int:
        stmt = select(func.count(Feed.id))
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        return result.scalar_one()

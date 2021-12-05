from typing import List, Optional

from sqlalchemy import func, delete
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from db.errors import EntityDoesNotExist
from db.repositories.base import BaseRepository
from models.feeds import Feed


class FeedsRepository(BaseRepository):
    model = Feed

    async def create(
            self,
            *,
            source_url: str,
            name: str,
            can_updated: bool
    ) -> Feed:

        new_feed = self.model(
            source_url=source_url,
            name=name,
            can_updated=can_updated,
        )

        self._session.add(new_feed)
        await self._session.flush()

        return new_feed

    async def delete(self, *, feed: Feed):
        stmt = delete(self.model).where(self.model.id == feed.id)
        await self._session.execute(stmt)
        await self._session.flush()

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
        await self._session.flush()

        return feed

    async def get_by_id(self, *, id_: int) -> Feed:
        stmt = select(self.model).where(self.model.id == id_)
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise EntityDoesNotExist(f'{self.model.__name__} with id = {id_} does not exist.')

    async def get_by_source_url(self, *, source_url: str) -> Feed:
        stmt = select(self.model).where(self.model.source_url == source_url)
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise EntityDoesNotExist(f'Feed with source_url = {source_url} not exist.')

    async def list_feeds(self, *, limit=20, offset=0) -> List[Feed]:
        stmt = select(self.model).order_by(-self.model.id).offset(offset).limit(limit)
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_total_count(self) -> int:
        stmt = select(func.count(self.model.id))
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        return result.scalar_one()

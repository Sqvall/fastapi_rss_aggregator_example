from typing import List

from sqlalchemy import func, delete, insert, update
from sqlalchemy.engine import ChunkedIteratorResult, CursorResult
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
        stmt = insert(Feed).values(source_url=source_url, name=name, can_updated=can_updated)
        stmt = stmt.returning(*Feed.__table__.columns)

        result: CursorResult = await self._session.execute(stmt)

        new_feed = result.first()
        return new_feed

    async def delete(self, *, feed: Feed):
        stmt = delete(self.model).where(self.model.id == feed.id)
        await self._session.execute(stmt)
        await self._session.flush()

    async def update(
            self,
            *,
            feed_id: id,
            **kwargs,
    ) -> Feed:
        stmt = update(Feed).values()
        for field, value in kwargs.items():
            stmt = stmt.values({field: value})

        stmt = stmt.where(Feed.id == feed_id).returning(*Feed.__table__.columns)

        result = await self._session.execute(stmt)

        updated_feed = result.first()

        return updated_feed

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
        stmt = select(self.model).order_by(-self.model.id).offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_total_count(self) -> int:
        stmt = select(func.count(self.model.id))
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        return result.scalar_one()

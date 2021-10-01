from __future__ import annotations

from typing import List

from sqlalchemy import func, desc
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.errors import EntityDoesNotExist
from app.db.repositories.base import BaseRepository
from app.models.entries import Entry


class EntriesRepository(BaseRepository):
    model = Entry

    async def add(self, entry: Entry) -> int:
        self._session.add(entry)
        await self._session.commit()

        return entry.id

    async def add_all(self, entries: List[Entry]) -> List[int]:
        self._session.add_all(entries)
        await self._session.commit()

        return [entry.id for entry in entries]

    async def get_entries(self, *, limit: int = 20, offset: int = 0, ) -> List[Entry]:
        stmt = (select(self.model)
                .order_by(desc(self.model.updated_at))
                .offset(offset)
                .limit(limit)
                .options(selectinload(self.model.tags), selectinload(self.model.feed)))

        result: ChunkedIteratorResult = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_by_id(self, *, id_: int) -> Entry:
        stmt = (select(self.model).where(self.model.id == id_)
                .options(selectinload(self.model.tags), selectinload(self.model.feed)))

        result: ChunkedIteratorResult = await self._session.execute(stmt)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise EntityDoesNotExist(f'{self.model.__name__} with id = {id_} does not exist.')

    async def get_total_count(self) -> int:
        stmt = select(func.count(self.model.id))
        result: ChunkedIteratorResult = await self._session.execute(stmt)

        return result.scalar_one()

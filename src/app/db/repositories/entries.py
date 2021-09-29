from sqlalchemy import func, insert
from sqlalchemy.engine import ChunkedIteratorResult, CursorResult
from sqlalchemy.future import select

from app.db.repositories.base import BaseRepository
from app.models.entries import Entry
from app.models.feeds import Feed


class EntriesRepository(BaseRepository):
    ...
    # async def create(
    #         self,
    #         *,
    #         link: str,
    #         guid: str = None,
    #         title: str = None,
    #         description: str = None,
    #         author: str = None,
    #         published_at: str = None,
    #         updated_at: str = None,
    # ) -> Entry:
    #     stmt = insert(Entry).values(
    #         source_url=source_url,
    #         name=name,
    #         can_updated=can_updated,
    #     ).returning(Feed)
    #
    #     result: CursorResult = await self._session.execute(stmt)
    #     await self._session.commit()
    #
    #     return result.first()
    #
    # async def get_total_count(self) -> int:
    #     stmt = select(func.count(Entry.id))
    #     result: ChunkedIteratorResult = await self._session.execute(stmt)
    #
    #     return result.scalar_one()

from typing import Type, Callable, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import async_session
from db.repositories.base import BaseRepository


async def _get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            yield session
            await session.commit()


def get_repository(repo_type: Type[BaseRepository]) -> Callable[[AsyncSession], BaseRepository]:
    def _set_session_for_repo(session: AsyncSession = Depends(_get_session)) -> BaseRepository:
        return repo_type(session)

    return _set_session_for_repo

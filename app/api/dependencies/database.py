from typing import Type, Callable, AsyncGenerator

from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import async_session
from db.repositories.base import BaseRepository


async def _get_session() -> AsyncGenerator[Session, None]:
    async with async_session() as session:
        async with session.begin():
            yield session


def get_repository(repo_type: Type[BaseRepository]) -> Callable[[Session], BaseRepository]:
    def _set_session_for_repo(session: Session = Depends(_get_session)) -> BaseRepository:
        return repo_type(session)

    return _set_session_for_repo

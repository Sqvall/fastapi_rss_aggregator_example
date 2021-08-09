from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    @property
    def session(self) -> AsyncSession:
        return self._db_session

from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    @property
    def session(self) -> Session:
        return self._db_session

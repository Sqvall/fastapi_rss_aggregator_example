from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f'<Tag(id={self.id!r}, name={self.name!r})>'

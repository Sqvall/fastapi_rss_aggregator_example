from sqlalchemy import Column, String, Text, Boolean, Integer
from sqlalchemy.orm import validates, relationship

from app.db.database import Base


class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True)
    source_url = Column(String, unique=True, nullable=False)
    name = Column(String)
    can_updated = Column(Boolean, default=True)
    title = Column(String, default='')
    description = Column(Text, default='')
    entries = relationship('Entry', back_populates='feed')

    @validates('name')
    def validate_name(self, _, name) -> str:
        if len(name) < 2:
            raise ValueError('\'name\' too short, this value has at least 2 characters.')
        return name

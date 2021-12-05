from sqlalchemy import Column, Integer, String, Text, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    guid = Column(String, nullable=True)
    link = Column(String)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    author = Column(String, nullable=True)
    published_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    feed_id = Column(Integer, ForeignKey('feeds.id'))
    feed = relationship('Feed', back_populates="entries")

    tags = relationship('Tag', secondary="entries_tags", backref="entries")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f'<Entry(id={self.id!r}, link={self.link!r}, feed={self.feed.name!r})>'


entries_tags_table = Table(
    'entries_tags', Base.metadata,
    Column('entry_id', ForeignKey('entries.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)

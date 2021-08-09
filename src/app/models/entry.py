from sqlalchemy import Column, Integer, String, Text, DateTime, func

from app.db.database import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    guid = Column(String, nullable=True)
    link = Column(String)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    author = Column(String, nullable=True)
    source = Column(String, nullable=True)
    pub_date_at = Column(DateTime(timezone=True), server_default=func.now())
    # for attr in ['title', 'title_detail', 'link']:
    # tag = relating to the Tags (m2m)
    # feed = relating to the Feed (m2o)

    def __str__(self):
        return f'<"id": "{self.id}", "title": "{self.title or self.guid or self.link}">'

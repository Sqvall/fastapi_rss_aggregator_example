from datetime import datetime
from typing import List

from pydantic import HttpUrl, validator

from app.schemas.common import CamelModel
from app.schemas.feeds import FeedShortOut
from app.schemas.tags import TagOut

DEFAULT_ENTRIES_LIMIT = 20
DEFAULT_ENTRIES_OFFSET = 0


class EntryOut(CamelModel):
    id: int
    link: HttpUrl
    feed: FeedShortOut
    guid: str
    title: str
    description: str
    author: str
    published_at: datetime
    updated_at: datetime
    tags: List[TagOut]

    @validator('published_at', 'updated_at', pre=True)
    def published_at_validate(cls, date):  # noqa
        if isinstance(date, datetime):
            return date.replace(tzinfo=None)
        return date

    class Config:
        orm_mode = True

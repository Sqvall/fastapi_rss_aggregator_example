from datetime import datetime
from typing import List, Optional

from pydantic import HttpUrl, validator

from schemas.common import CamelModel
from schemas.feeds import FeedShortOut
from schemas.tags import TagOut

DEFAULT_ENTRIES_LIMIT = 20
DEFAULT_ENTRIES_OFFSET = 0


class EntryOut(CamelModel):
    id: int
    link: HttpUrl
    feed: FeedShortOut
    guid: Optional[str]
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]
    published_at: datetime
    updated_at: datetime
    tags: Optional[List[TagOut]]

    @validator('published_at', 'updated_at', pre=True)
    def published_at_validate(cls, date):  # noqa
        if isinstance(date, datetime):
            return date.replace(tzinfo=None)
        return date

    class Config:
        orm_mode = True

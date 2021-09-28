from typing import Optional

from pydantic import Field, HttpUrl

from app.schemas.common import CamelModel
from app.resources import strings

DEFAULT_FEEDS_LIMIT = 20
DEFAULT_FEEDS_OFFSET = 0


class FeedInCreate(CamelModel):
    source_url: HttpUrl = Field(..., example=strings.EXAMPLE_SOURCE_URL)
    name: str = Field(..., example=strings.EXAMPLE_NAME, min_length=2)
    can_updated: bool = Field(..., description=strings.DESCRIPTION_CAN_UPDATED)


class FeedInUpdate(CamelModel):
    source_url: Optional[HttpUrl] = Field(default=None, example=strings.EXAMPLE_SOURCE_URL)
    name: Optional[str] = Field(default=None, example=strings.EXAMPLE_NAME, min_length=2)
    can_updated: Optional[bool] = Field(default=None, description=strings.DESCRIPTION_CAN_UPDATED)
    title: Optional[str]
    description: Optional[str]


class FeedOut(CamelModel):
    id: int
    source_url: HttpUrl
    name: str
    can_updated: bool
    title: str
    description: str

    class Config:
        orm_mode = True

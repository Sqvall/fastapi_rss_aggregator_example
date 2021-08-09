from typing import Optional

from pydantic import AnyUrl, Field

from app.models.camelmodel import CamelModel
from app.resources import strings


class FeedInCreate(CamelModel):
    source_url: AnyUrl = Field(..., example=strings.EXAMPLE_SOURCE_URL)
    name: str = Field(..., example=strings.EXAMPLE_NAME, min_length=2)
    can_updated: bool = Field(..., description=strings.DESCRIPTION_CAN_UPDATED)


class FeedInUpdate(CamelModel):
    source_url: Optional[AnyUrl] = Field(default=None, example=strings.EXAMPLE_SOURCE_URL)
    name: Optional[str] = Field(default=None, example=strings.EXAMPLE_NAME, min_length=2)
    can_updated: Optional[bool] = Field(default=None, description=strings.DESCRIPTION_CAN_UPDATED)
    title: Optional[str]
    description: Optional[str]


class FeedOut(CamelModel):
    id: int
    source_url: AnyUrl
    name: str
    can_updated: bool
    title: str
    description: str

    class Config:
        orm_mode = True

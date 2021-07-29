from typing import Optional

from pydantic import BaseModel, AnyUrl, Field


class FeedIn(BaseModel):
    source_url: AnyUrl = Field(..., example='https://github.com/images/error/octocat_happy.gif')
    name: str = Field(..., example='Name for identification.')
    can_updated: bool = Field(..., description='Add for regular updates?')


class FeedOut(FeedIn):
    title: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True

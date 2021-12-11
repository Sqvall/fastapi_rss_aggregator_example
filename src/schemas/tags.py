from schemas.common import CamelModel


class TagOut(CamelModel):
    id: int
    name: str

    class Config:
        orm_mode = True


from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

from models.test_tortouse import User_Pydantic, Users, UserIn_Pydantic

router = APIRouter()

class Status(BaseModel):
    message: str


@router.get("/users", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.post("/users", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))
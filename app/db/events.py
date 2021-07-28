from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from core.config import TORTOISE_ORM


async def connect_to_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        add_exception_handlers=True,
    )

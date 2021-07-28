from typing import Callable

from fastapi import FastAPI

from db.events import connect_to_db


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app

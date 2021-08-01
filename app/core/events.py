from typing import Callable

from db.events import connect_to_db, disconnect_from_db


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        await connect_to_db()

    return start_app


def create_shutdown_app_handler() -> Callable:
    async def start_app() -> None:
        await disconnect_from_db()

    return start_app

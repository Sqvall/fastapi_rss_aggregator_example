from db.database import async_engine, Base


async def connect_to_db() -> None:
    async with async_engine.begin() as conn:
        ...
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)


async def disconnect_from_db() -> None:
    ...

from db.database import async_engine, Base


async def connect_to_db() -> None:
    # async with async_engine.begin() as conn: # TODO: Research this!
    ...
    #     await conn.run_sync(Base.metadata.create_all)
    #     await conn.run_sync(Base.metadata.drop_all)


async def disconnect_from_db() -> None:
    ...

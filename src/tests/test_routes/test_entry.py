from typing import List

import pytest
from starlette import status

from app.db.repositories.entries import EntriesRepository
from app.models import Entry
from app.schemas.entries import EntryOut, DEFAULT_ENTRIES_LIMIT
from tests.factories import EntryFactory
from tests.testing_helpers import destructuring_pagination

pytestmark = pytest.mark.asyncio


async def test_get_empty_list_entries_if_not_one(client, app):
    response = await client.get(app.url_path_for('entries:list-entries'))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'items': [], 'itemsTotal': 0}


async def test_get_list_entries_correct_data(client, app, session, entry_factory: EntryFactory):
    entry_rep = EntriesRepository(session)
    factory_data: List[Entry] = entry_factory.create_batch(10)

    await entry_rep.add_all(factory_data)

    exp_data = [EntryOut.from_orm(entry) for entry in await entry_rep.get_entries(limit=20, offset=0)]

    response = await client.get(app.url_path_for('entries:list-entries'))
    items, items_total = destructuring_pagination(response.json())

    assert items_total == len(exp_data)
    assert len(items) == len(exp_data)

    for i in range(len(exp_data)):
        assert EntryOut(**items[i]) == exp_data[i]


async def test_list_feed_default_pagination(session, client, app, entry_factory: EntryFactory):
    entry_rep = EntriesRepository(session)
    factory_data: List[Entry] = entry_factory.create_batch(50)

    await entry_rep.add_all(factory_data)
    exp_data = await entry_rep.get_entries(limit=1, offset=0)

    response = await client.get(app.url_path_for('entries:list-entries'))
    items, items_total = destructuring_pagination(response.json())

    assert len(items) == DEFAULT_ENTRIES_LIMIT
    assert items_total == 50
    assert items[0]['link'] == exp_data[0].link


@pytest.mark.parametrize(
    "offset, limit",
    [(0, 10), (10, 10), (20, 20), (40, 20), (99, 1)]
)
async def test_list_feed_pagination(session, client, app, entry_factory: EntryFactory, offset, limit):
    pagination = {'offset': offset, 'limit': limit}
    feeds_count = 60

    entry_rep = EntriesRepository(session)
    factory_data: List[Entry] = entry_factory.create_batch(feeds_count)

    await entry_rep.add_all(factory_data)
    exp_data = await entry_rep.get_entries(**pagination)

    response = await client.get(app.url_path_for('entries:list-entries'), params=pagination)
    items, items_total = destructuring_pagination(response.json())

    exp_len_data = limit

    if (offset + limit) > feeds_count:
        exp_len_data = max(0, feeds_count - offset)

    assert len(items) == exp_len_data
    assert items_total == feeds_count

    if len(items):
        assert items[0]['link'] == exp_data[0].link
        assert items[-1]['link'] == exp_data[-1].link


async def test_get_entry_by_id(session, client, app, entry_factory: EntryFactory):
    entry_rep = EntriesRepository(session)
    entry = entry_factory.create()
    entry_id = await entry_rep.add(entry)
    entry_db = await entry_rep.get_by_id(id_=entry_id)

    response = await client.get(url=app.url_path_for('entries:get-entry', entry_id=str(entry_id)))

    received_entry_out = EntryOut(**response.json())
    entry_db_out = EntryOut.from_orm(entry_db)

    assert received_entry_out == entry_db_out


async def test_get_feed_by_id_return_404_if_feed_not_exist(client, app):
    response = await client.get(url=app.url_path_for('feeds:get-feed', feed_id=str(-1)))

    assert response.status_code == status.HTTP_404_NOT_FOUND

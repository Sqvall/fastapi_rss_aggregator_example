from typing import List

import pytest
from starlette import status

from db.repositories import EntriesRepository
from db.repositories import FeedsRepository
from models import Entry
from schemas.entries import EntryOut, DEFAULT_ENTRIES_LIMIT
from tests.factories import EntryRelatedFactory, EntryBaseFactory, TagFactory, FeedFactory
from tests.testing_helpers import destructuring_pagination

pytestmark = pytest.mark.asyncio


async def test_get_empty_list_entries_if_not_one(client, app):
    response = await client.get(app.url_path_for('entries:list-entries'))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'items': [], 'itemsTotal': 0}


async def test_get_list_entries_correct_data(
        session,
        client,
        app,
        entry_related_factory: EntryRelatedFactory
):
    entry_rep = EntriesRepository(session)
    factory_data: List[Entry] = entry_related_factory.create_batch(10)

    await entry_rep.add_all(factory_data)

    exp_data = [EntryOut.from_orm(entry) for entry in await entry_rep.list_entries(limit=20, offset=0)]

    response = await client.get(app.url_path_for('entries:list-entries'))
    items, items_total = destructuring_pagination(response.json())

    assert items_total == len(exp_data)
    assert len(items) == len(exp_data)

    for i in range(len(exp_data)):
        assert EntryOut(**items[i]) == exp_data[i]


async def test_list_feed_default_pagination(
        session,
        client,
        app,
        entry_related_factory: EntryRelatedFactory
):
    entry_rep = EntriesRepository(session)
    factory_data: List[Entry] = entry_related_factory.create_batch(50)

    await entry_rep.add_all(factory_data)
    exp_data = await entry_rep.list_entries(limit=1, offset=0)

    response = await client.get(app.url_path_for('entries:list-entries'))
    items, items_total = destructuring_pagination(response.json())

    assert len(items) == DEFAULT_ENTRIES_LIMIT
    assert items_total == 50
    assert items[0]['link'] == exp_data[0].link


@pytest.mark.parametrize(
    "offset, limit",
    [(0, 10), (20, 20), (40, 20), (99, 1), (10, 1), (0, 1)]
)
async def test_list_feed_pagination(
        session,
        client,
        app,
        entry_related_factory: EntryRelatedFactory,
        offset,
        limit
):
    pagination = {'offset': offset, 'limit': limit}
    feeds_count = 60

    entry_rep = EntriesRepository(session)
    factory_data: List[Entry] = entry_related_factory.create_batch(feeds_count)

    await entry_rep.add_all(factory_data)
    exp_data = await entry_rep.list_entries(**pagination)

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


async def test_get_list_entries_filtered_by_tags(
        session,
        client,
        app,
        feed_factory: FeedFactory,
        tag_factory: TagFactory,
        entry_base_factory: EntryBaseFactory,
):
    feed = feed_factory.create()
    tag1, tag2, tag3 = tag_factory.create_batch(3)

    entries = entry_base_factory.create_batch(10)
    for i in range(len(entries)):
        entries[i].feed = feed
        entries[i].tags.append(tag1)
        if i % 2 == 0:
            entries[i].tags.append(tag2)
        if i % 3 == 0:
            entries[i].tags.append(tag3)

    entry_repo = EntriesRepository(session)
    await entry_repo.add_all(entries)

    params_four_entries = {'tag_ids': [tag3.id]}
    response = await client.get(app.url_path_for('entries:list-entries'), params=params_four_entries)
    four_items, _ = destructuring_pagination(response.json())
    assert len(four_items) == 4

    params_five_entries = {'tag_ids': [tag2.id]}
    response = await client.get(app.url_path_for('entries:list-entries'), params=params_five_entries)
    five_items, _ = destructuring_pagination(response.json())
    assert len(five_items) == 5

    params_ten_entries = {'tag_ids': [tag1.id]}
    response = await client.get(app.url_path_for('entries:list-entries'), params=params_ten_entries)
    ten_items, _ = destructuring_pagination(response.json())
    assert len(ten_items) == 10

    params_seven_entries = {'tag_ids': [tag2.id, tag3.id]}
    response = await client.get(app.url_path_for('entries:list-entries'), params=params_seven_entries)
    seven_items, _ = destructuring_pagination(response.json())
    assert len(seven_items) == 7


@pytest.mark.parametrize(
    'first_entries_count, second_entries_count',
    ((5, 7), (0, 2), (15, 0), (0, 0))
)
async def test_list_entries_filtered_by_feed(
        session,
        client,
        app,
        feed_factory: FeedFactory,
        entry_base_factory: EntryBaseFactory,
        first_entries_count,
        second_entries_count,
):
    entry_repo = EntriesRepository(session)
    feed_repo = FeedsRepository(session)

    feed1 = feed_factory.create()
    feed1 = await feed_repo.create(source_url=feed1.source_url, name=feed1.name, can_updated=feed1.can_updated)
    first_entries_set = entry_base_factory.create_batch(first_entries_count, feed=feed1)
    await entry_repo.add_all(first_entries_set)

    feed2 = feed_factory.create()
    feed2 = await feed_repo.create(source_url=feed2.source_url, name=feed2.name, can_updated=feed2.can_updated)
    second_entries_set = entry_base_factory.create_batch(second_entries_count, feed=feed2)
    await entry_repo.add_all(second_entries_set)

    params_five_entries = {'feed_id': [feed1.id]}
    response = await client.get(app.url_path_for('entries:list-entries'), params=params_five_entries)
    first_items, _ = destructuring_pagination(response.json())
    assert len(first_items) == first_entries_count

    params_seven_entries = {'feed_id': [feed2.id]}
    response = await client.get(app.url_path_for('entries:list-entries'), params=params_seven_entries)
    second_items, _ = destructuring_pagination(response.json())
    assert len(second_items) == second_entries_count


async def test_get_entry_by_id(
        session,
        client,
        app,
        entry_related_factory: EntryRelatedFactory
):
    entry_rep = EntriesRepository(session)
    entry = entry_related_factory.create()
    entry_id = await entry_rep.add(entry)
    entry_db = await entry_rep.get_by_id(id_=entry_id)

    response = await client.get(url=app.url_path_for('entries:get-entry', entry_id=str(entry_id)))

    received_entry_out = EntryOut(**response.json())
    entry_db_out = EntryOut.from_orm(entry_db)

    assert received_entry_out == entry_db_out


async def test_get_entry_by_id_return_404_if_feed_not_exist(client, app):
    response = await client.get(url=app.url_path_for('entries:get-entry', entry_id=str(-1)))

    assert response.status_code == status.HTTP_404_NOT_FOUND

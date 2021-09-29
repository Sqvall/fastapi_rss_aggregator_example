import pytest
from starlette import status

from app.db.errors import EntityDoesNotExist
from app.db.repositories.feeds import FeedsRepository
from app.models.feeds import Feed
from app.schemas.feeds import FeedOut, DEFAULT_FEEDS_LIMIT
from tests.testing_helpers import destructuring_pagination

pytestmark = pytest.mark.asyncio


async def test_can_create_feed(client, app, session):
    feed_data = {
        "sourceUrl": "https://example.com",
        "name": "Test Name 01",
        "canUpdated": True,
    }
    response = await client.post(url=app.url_path_for('feeds:create-feed'), json=feed_data)

    assert response.status_code == status.HTTP_201_CREATED

    received_feed_out = FeedOut(**response.json())
    feed_from_db = await FeedsRepository(session).get_by_source_url(source_url=received_feed_out.source_url)
    received_feed_from_db_out = FeedOut.from_orm(feed_from_db)

    assert received_feed_out == received_feed_from_db_out


async def test_create_raise_400_if_feed_with_source_url_exist(client, app, test_feed: Feed):
    new_feed = {
        "sourceUrl": test_feed.source_url,
        "name": "Test Name 13",
        "canUpdated": False,
    }

    response = await client.post(url=app.url_path_for('feeds:create-feed'), json=new_feed)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_get_empty_list_when_no_one_feed_created(client, app):
    response = await client.get(app.url_path_for('feeds:list-feeds'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'items': [], 'itemsTotal': 0}


async def test_get_list_feed_correct_data(client, app, session):
    exp_data = [
        {'source_url': 'https://example1.com', 'name': 'Some name 1', 'can_updated': True},
        {'source_url': 'https://example2.com', 'name': 'Some name 2', 'can_updated': False},
        {'source_url': 'https://example3.com', 'name': 'Some name 3', 'can_updated': True}
    ]

    feed_rep = FeedsRepository(session)
    await feed_rep.create(**exp_data[2])
    await feed_rep.create(**exp_data[1])
    await feed_rep.create(**exp_data[0])

    response = await client.get(app.url_path_for('feeds:list-feeds'))
    items, items_total = destructuring_pagination(response.json())

    assert len(items) == len(exp_data)
    assert items_total == len(exp_data)

    for i in range(len(exp_data)):
        assert set(items[i].values()) >= set(exp_data[i].values())


async def test_list_feed_default_pagination(client, app, create_50_feeds):
    response = await client.get(app.url_path_for('feeds:list-feeds'))
    items, items_total = destructuring_pagination(response.json())

    assert len(items) == DEFAULT_FEEDS_LIMIT
    assert items_total == 50
    assert items[0]['name'] == 'Some name 50'


@pytest.mark.parametrize(
    "offset, limit",
    [(0, 10), (10, 10), (20, 20), (40, 20), (99, 1)]
)
async def test_list_feed_pagination(client, app, create_50_feeds, offset, limit):
    pagination = {'offset': offset, 'limit': limit}

    response = await client.get(app.url_path_for('feeds:list-feeds'), params=pagination)
    items, items_total = destructuring_pagination(response.json())

    feeds_count = 50
    exp_len_data = limit

    if (offset + limit) > feeds_count:
        exp_len_data = max(0, feeds_count - offset)

    first_feed_number = feeds_count - offset
    last_feed_number = first_feed_number - exp_len_data + 1

    assert len(items) == exp_len_data
    assert items_total == feeds_count

    if len(items):
        assert items[0]['name'] == f'Some name {first_feed_number}'
        assert items[-1]['name'] == f'Some name {last_feed_number}'


async def test_get_feed_by_id(client, app, test_feed: Feed):
    response = await client.get(url=app.url_path_for('feeds:get-feed', feed_id=str(test_feed.id)))

    received_feed_out = FeedOut(**response.json())

    assert received_feed_out.id == test_feed.id
    assert received_feed_out.source_url == test_feed.source_url
    assert received_feed_out.name == test_feed.name


async def test_get_feed_by_id_return_404_if_feed_not_exist(client, app):
    response = await client.get(url=app.url_path_for('feeds:get-feed', feed_id=str(-1)))

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_feed(client, app, session, test_feed: Feed):
    # TODO: Need more test cases (not requirement, None, ...etc)
    updated_feed_data = {
        "sourceUrl": "https://example.com/updated",
        "name": "Updated Test Name",
        "canUpdated": False,
        "title": "Updated Title",
        "description": "Updated Description",
    }

    response = await client.put(
        url=app.url_path_for('feeds:update-feed', feed_id=str(test_feed.id)),
        json={"feed": updated_feed_data}
    )

    updated_feed_data["id"] = test_feed.id

    assert response.json() == updated_feed_data


@pytest.mark.parametrize(
    'field, value',
    [
        ('sourceUrl', 'https://example.com/updated13'),
        ('name', 'Some test name for update'),
        ('canUpdated', False),
        ('canUpdated', True),
        ('title', 'Some test title 13'),
        ('description', 'Some test desc 13'),
    ]
)
async def test_update_feed_for_one_field(client, app, session, test_feed: Feed, field, value):
    response = await client.put(
        url=app.url_path_for('feeds:update-feed', feed_id=str(test_feed.id)),
        json={"feed": {field: value}}
    )

    assert response.json()[field] == value


async def test_update_raise_400_if_feed_with_source_url_exist(client, app, session, test_feed: Feed):
    updated_new_feed_data = {
        "sourceUrl": test_feed.source_url,
    }

    new_feed = {
        "source_url": "https://example.com",
        "name": "Test Name 13",
        "can_updated": False,
    }

    new_feed = await FeedsRepository(session).create(**new_feed)

    response = await client.put(
        url=app.url_path_for('feeds:update-feed', feed_id=str(new_feed.id)),
        json={"feed": updated_new_feed_data}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_delete_feed(client, app, session, test_feed: Feed):
    response = await client.delete(url=app.url_path_for('feeds:delete', feed_id=str(test_feed.id)))

    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(EntityDoesNotExist):
        await FeedsRepository(session).get_by_id(id_=test_feed.id)

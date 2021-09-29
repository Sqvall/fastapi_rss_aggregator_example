import pytest
from starlette import status

from app.models.feeds import Feed

pytestmark = pytest.mark.asyncio


async def test_get_empty_list_entries_if_not_one(client, app):
    response = await client.get(app.url_path_for('entries:list-entries'))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'items': [], 'itemsTotal': 0}


# async def test_get_list_entries_correct_data(client, app, session, test_feed: Feed, test_tag: Tag):
async def test_get_list_entries_correct_data(client, app, session, test_feed: Feed):
    exp_data = [
        {
            # 'id': 1,
            'guid': 'https://example.com/872134',
            'link': 'https://example.com/test13link',
            'title': 'Test title',
            'description': 'Test description',
            'author': 'Test Author',
            'publish_at': 'Wed, 29 Sep 2021 07:00:00 GMT',
            'update_at': 'Wed, 29 Sep 2021 07:00:00 GMT',
            'tags': [
                {
                    'id': 113,
                    'name': 'Test category name',
                }
            ],
            'sources': test_feed
        },
    ]

    # entry_rep = EntriesRepository(session)
    # await entry_rep.create(**exp_data[2])
    # await entry_rep.create(**exp_data[1])
    # await entry_rep.create(**exp_data[0])
    #
    # response = await client.get(app.url_path_for('entries:list-entries'))
    # items, items_total = destructuring_pagination(response.json())
    #
    # assert items_total == len(exp_data)
    # assert len(items) == len(exp_data)
    #
    # for i in range(len(exp_data)):
    #     assert set(items[i].values()) >= set(exp_data[i].values())

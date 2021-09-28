from operator import itemgetter


def destructuring_pagination(data: dict):
    items, items_total_count = itemgetter('items', 'itemsTotal')(data)
    return items, items_total_count

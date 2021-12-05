import factory
from faker import Faker

from models import Tag, Feed, Entry

faker = Faker()


class FeedFactory(factory.Factory):
    class Meta:
        model = Feed

    source_url = factory.Sequence(lambda n: faker.url() + str(n))
    name = faker.sentence(nb_words=5)
    can_updated = faker.boolean()


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: faker.word() + str(n))


class EntryBaseFactory(factory.Factory):
    class Meta:
        model = Entry

    link = factory.Sequence(lambda n: faker.url() + str(n))
    guid = faker.uuid4()
    title = factory.Sequence(lambda n: faker.sentence(nb_words=10))
    description = faker.sentence(nb_words=50)
    author = faker.name()
    published_at = factory.Sequence(lambda n: faker.date_time())
    updated_at = factory.Sequence(lambda n: faker.date_time())


class EntryRelatedFactory(EntryBaseFactory):
    feed = factory.SubFactory(FeedFactory)
    tags = factory.List([factory.SubFactory(TagFactory) for _ in range(5)])

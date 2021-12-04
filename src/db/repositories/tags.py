from db.repositories.base import BaseRepository
from models import Tag
from models.entries import Entry


class TagsRepository(BaseRepository):

    async def create(
            self,
            *,
            name: str,
    ) -> Entry:
        new_tag = Tag(
            name=name,
        )

        self._session.add(new_tag)
        await self._session.commit()

        return new_tag

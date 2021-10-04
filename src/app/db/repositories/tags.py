from app.db.repositories.base import BaseRepository
from app.models import Tag
from app.models.entries import Entry


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

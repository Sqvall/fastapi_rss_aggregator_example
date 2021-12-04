from fastapi import Path, Depends, HTTPException
from starlette import status

from api.dependencies.database import get_repository
from db.errors import EntityDoesNotExist
from db.repositories.entries import EntriesRepository
from models import Entry
from resources import strings


async def get_entry_by_id_from_path(
        entry_id: int = Path,
        entries_repo: EntriesRepository = Depends(get_repository(EntriesRepository)),
) -> Entry:
    try:
        return await entries_repo.get_by_id(id_=entry_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.ENTRY_DOES_NOT_EXIST_ERROR,
        )

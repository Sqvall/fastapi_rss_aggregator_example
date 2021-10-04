from typing import List

from fastapi import APIRouter, Query, Depends
from starlette import status

from app.api.dependencies.database import get_repository
from app.api.dependencies.entry import get_entry_by_id_from_path
from app.db.repositories.entries import EntriesRepository
from app.models import Entry
from app.schemas.common import PaginatedResponse
from app.schemas.entries import EntryOut, DEFAULT_ENTRIES_LIMIT, DEFAULT_ENTRIES_OFFSET

router = APIRouter()


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[EntryOut],
    name='entries:list-entries',
)
async def list_entry(
        entry_repo: EntriesRepository = Depends(get_repository(EntriesRepository)),
        tag_ids: List[int] = Query(None),
        feed_id: int = Query(None),
        limit: int = Query(DEFAULT_ENTRIES_LIMIT, ge=1),
        offset: int = Query(DEFAULT_ENTRIES_OFFSET, ge=0),
):
    entries = await entry_repo.list_entries(tag_ids=tag_ids, feed_id=feed_id, limit=limit, offset=offset)
    total_count = await entry_repo.get_total_count()
    return PaginatedResponse[EntryOut](items=entries, items_total=total_count)


@router.get(
    '/{entry_id}',
    status_code=status.HTTP_200_OK,
    response_model=EntryOut,
    name='entries:get-entry',
)
async def retrieve_entry_by_id(entry: Entry = Depends(get_entry_by_id_from_path)):
    return entry

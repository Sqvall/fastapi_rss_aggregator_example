from fastapi import APIRouter, Query
from starlette import status

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
        limit: int = Query(DEFAULT_ENTRIES_LIMIT, ge=1),
        offset: int = Query(DEFAULT_ENTRIES_OFFSET, ge=0),
):
    entries = []
    return PaginatedResponse[EntryOut](items=entries, items_total=0)

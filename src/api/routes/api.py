from fastapi import APIRouter

from api.routes import feeds, main_page, entries

router = APIRouter()
router.include_router(main_page.router, tags=['main'])
router.include_router(feeds.router, tags=['feeds'], prefix='/feeds')
router.include_router(entries.router, tags=['entries'], prefix='/entries')

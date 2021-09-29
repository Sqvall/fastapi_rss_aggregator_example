from fastapi import APIRouter

from app.api.routes import main_page
from app.api.routes import feeds, entries

router = APIRouter()
router.include_router(main_page.router, tags=['main'])
router.include_router(feeds.router, tags=['feeds'], prefix='/feeds')
router.include_router(entries.router, tags=['entries'], prefix='/entries')

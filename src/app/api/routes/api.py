from fastapi import APIRouter

from app.api.routes import main_page
from app.api.routes import feeds

router = APIRouter()
router.include_router(main_page.router, tags=['main'])
router.include_router(feeds.router, tags=['feeds'], prefix='/feeds')

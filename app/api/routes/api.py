from fastapi import APIRouter

from api.routes import main_page
from api.routes.feeds import feed_router

router = APIRouter()
router.include_router(main_page.router, tags=['main'])
router.include_router(feed_router, tags=['feeds'], prefix='/feeds')

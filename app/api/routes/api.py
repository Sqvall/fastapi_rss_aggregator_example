from fastapi import APIRouter

from api.routes import main_page, test_tortouse, feeds

router = APIRouter()
router.include_router(main_page.router, tags=['main'])
router.include_router(test_tortouse.router, tags=['user'])
router.include_router(feeds.router, tags=['feeds'], prefix='/feeds')

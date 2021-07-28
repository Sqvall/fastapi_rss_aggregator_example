from fastapi import APIRouter

from api.routes import main_page, test_tortouse

router = APIRouter()
router.include_router(main_page.router, tags=['main'])
router.include_router(test_tortouse.router, tags=['user'])

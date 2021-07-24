from fastapi import APIRouter

from api.routes import main_page

router = APIRouter()
router.include_router(main_page.router, tags=['main'])

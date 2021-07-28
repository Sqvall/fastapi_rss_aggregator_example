from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes.api import router as api_router
from core import config
from core.events import create_start_app_handler


def get_application() -> FastAPI:

    application = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler(application))

    application.include_router(api_router, prefix=config.API_PREFIX)

    return application


app = get_application()

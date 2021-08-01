from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from api.errors.http_error import http_error_handler
from api.errors.validation_error import http422_error_handler
from api.routes.api import router as api_router
from core import config
from core.events import create_start_app_handler, create_shutdown_app_handler


def get_application() -> FastAPI:
    application = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler())
    application.add_event_handler("shutdown", create_shutdown_app_handler())

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=config.API_PREFIX)

    return application


app = get_application()

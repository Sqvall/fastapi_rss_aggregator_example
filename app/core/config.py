from typing import List

from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Token"
VERSION = "0.0.0"

config = Config('.env')

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)
if TESTING:
    DATABASE_URL = DATABASE_URL.replace(database='test_' + DATABASE_URL.database)
# MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
# MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)


PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example RSS-aggregator application")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# logging configuration

# LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
# LOGGERS = ("uvicorn.asgi", "uvicorn.access")
#
# logging.getLogger().handlers = [InterceptHandler()]
# for logger_name in LOGGERS:
#     logging_logger = logging.getLogger(logger_name)
#     logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]
#
# logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

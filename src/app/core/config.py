import logging
import os
import pathlib

from sqlalchemy.engine.url import make_url, URL
from starlette.config import Config
from starlette.datastructures import Secret, CommaSeparatedStrings

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.propagate = False

env_path = os.path.join(pathlib.Path(__file__).parent.absolute(), '../../../.env')

config = Config(env_path)

PROJECT_NAME = "FastAPI example RSS-aggregator application"
API_PREFIX = "/api"
VERSION = "0.1.0"
JWT_TOKEN_PREFIX = "Token"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default=None)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=['*'])

DEBUG = config("DEBUG", cast=bool, default=True)
TESTING = config("TESTING", cast=bool, default=False)

# Config DB
DB_DRIVER = config("DB_DRIVER", default="postgresql+asyncpg")
DB_HOST = config("DB_HOST", default=None)
DB_PORT = config('DB_PORT', cast=int, default=5432)
DB_USER = config('DB_USER', default=None)
DB_PASSWORD = config('DB_PASSWORD', default=None)
DB_NAME = config('DB_NAME' if not TESTING else 'TEST_DB_NAME', default=None)
DB_URL = config(
    "DB_DSN",
    cast=make_url,
    default=URL.create(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    ),
)

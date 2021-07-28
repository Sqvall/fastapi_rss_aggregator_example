import logging
import os
import pathlib

from starlette.config import Config
from starlette.datastructures import Secret, CommaSeparatedStrings

log = logging.getLogger("uvicorn")

env_path = os.path.join(pathlib.Path(__file__).parent.absolute(), '../../.env')

config = Config(env_path)

PROJECT_NAME = "FastAPI example RSS-aggregator application"
API_PREFIX = "/api"
VERSION = "0.1.0"
JWT_TOKEN_PREFIX = "Token"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default=None)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=['*'])

DEBUG = config("DEBUG", cast=bool, default=True)
TESTING = config("DEBUG", cast=bool, default=False)

# Config DB
DB_ENGINE = config("DB_DRIVER", default="tortoise.backends.asyncpg")
DB_HOST = config("DB_HOST", default=None)
DB_PORT = config('DB_PORT', cast=int, default=5432)
DB_USER = config('DB_USER', default=None)
DB_PASSWORD = config('DB_PASSWORD', default=None)
DB_NAME = config('DB_NAME', default=None)
TORTOISE_ORM = {
    "connections": {"default": {
        'engine': DB_ENGINE,
        'credentials': {
            'host': DB_HOST,
            'port': DB_PORT,
            'user': DB_USER,
            'password': DB_PASSWORD,
            'database': DB_NAME,
        }
    }},
    "apps": {
        "models": {
            "models": [
                'models.test_tortouse',
                'aerich.models'
            ],
        }
    }
}
# DATABASE_URL: str = 'postgres://rss_user:pass@localhost:5432/rss_local_db'
# if TESTING:
#     DATABASE_URL = 'test_' + DATABASE_URL

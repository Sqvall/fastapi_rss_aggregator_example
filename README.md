### Proget not complete, but you can use it for your ideas.

## Create local db

```sql
CREATE USER rss_user WITH ENCRYPTED PASSWORD 'pass';
CREATE DATABASE rss_local_db OWNER rss_user;
CREATE DATABASE test_rss_local_db OWNER rss_user;
```

## Start app

- Python 3.9 + poetry

After:
```shell
cp .env.example .env
```

Edit `.env` and set variables.

```shell
cd src
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --host=0.0.0.0 --port=8000
```

## Start app in docker

```shell
cp .env.example .env
```

```shell
dokcer-compose up --build
```

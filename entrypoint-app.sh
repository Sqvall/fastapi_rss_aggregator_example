#!/usr/bin/env bash
while ! </dev/tcp/db/5432
do
  sleep 1
done

poetry run alembic upgrade head
poetry run uvicorn app.main:app --host=0.0.0.0 --port=8020
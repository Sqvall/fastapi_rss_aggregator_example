#!/usr/bin/env bash
while ! </dev/tcp/db/5432
do
  sleep 1
done

aerich upgrade
uvicorn main:app --host=0.0.0.0 --port=8020
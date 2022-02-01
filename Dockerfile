FROM python:3.9.6-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

WORKDIR /app
COPY ./src/poetry.lock ./src/pyproject.toml /app/

RUN pip install --upgrade pip && \
    pip install poetry==1.1.10 && \
    poetry config virtualenvs.create false && \
    poetry install

COPY ./src /app

EXPOSE 8020

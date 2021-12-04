FROM python:3.9.6-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

WORKDIR /app
COPY ./src /app

RUN pip install --upgrade pip && \
    pip install poetry==1.1.10 && \
    poetry config virtualenvs.create false && \
    poetry install

RUN groupadd -r rss_uvicorn && \
    useradd -r -g rss_uvicorn rss_uvicorn

USER rss_uvicorn

EXPOSE 8020

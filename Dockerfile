FROM python:3.9.6-slim

ENV PYTHONUNBUFFERED 1

RUN groupadd -r rss_uviconr && \
    useradd -r -g rss_uviconr rss_uviconr

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app
COPY requirements.txt ./
COPY app ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

USER rss_uviconr
CMD uvicorn --host=0.0.0.0 --port=8020 main:app
EXPOSE 8020

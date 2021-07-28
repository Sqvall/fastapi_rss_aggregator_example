FROM python:3.9.6-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /src
COPY requirements.txt ./
COPY . ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

RUN groupadd -r rss_uviconr && \
    useradd -r -g rss_uviconr rss_uviconr

USER rss_uviconr
WORKDIR /src/app
COPY entrypoint-app.sh ./
EXPOSE 8020

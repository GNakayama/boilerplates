FROM python:3.10.5-slim

RUN useradd -ms /bin/bash appuser

RUN apt-get update && apt-get install -y libpq-dev gcc libcurl4-openssl-dev libssl-dev

WORKDIR /app

COPY ./requirements-dev.txt /tmp/requirements-dev.txt
COPY ./requirements.txt /tmp/requirements.txt
RUN cd /tmp/ && pip install -r requirements-dev.txt

COPY --chown=appuser:appuser . /app

USER appuser

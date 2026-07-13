from python:3.13-slim

ENV PYTHONDONTWITEBYTECODE=1
ENV PYTHONUNBUFEERED=1

WORKDIR /app

RUN apt-get update &&
apt-get install -t
--no-install-recommends \gcc \libqp-dev \&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/run pip install --no-cache-dir-r requirements.txt

COPY . /app/

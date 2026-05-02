FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make fontconfig ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

# Python deps
RUN pip install --no-cache-dir numpy matplotlib pandas requests

WORKDIR /work
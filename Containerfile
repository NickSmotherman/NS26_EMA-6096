FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make fontconfig fonts-liberation ca-certificates curl xz-utils && \
    rm -rf /var/lib/apt/lists/*

# Typst CLI (detect arch)
ARG TYPST_VERSION=0.12.0
RUN ARCH=$(uname -m) && \
    case "$ARCH" in \
        x86_64)  TARGET="x86_64-unknown-linux-musl" ;; \
        aarch64) TARGET="aarch64-unknown-linux-musl" ;; \
        *) echo "Unsupported: $ARCH" && exit 1 ;; \
    esac && \
    curl -fsSL "https://github.com/typst/typst/releases/download/v${TYPST_VERSION}/typst-${TARGET}.tar.xz" \
        | tar -xJf - --strip-components=1 -C /usr/local/bin && \
    typst --version

# Python deps
RUN pip install --no-cache-dir numpy matplotlib pandas requests scipy

WORKDIR /work
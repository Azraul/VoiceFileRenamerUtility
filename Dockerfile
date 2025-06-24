# Dockerfile
# First test of Multi-stage build, two stages
# https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/

# STAGE 1: Whisper.cpp build
## Full Ubuntu env
FROM ubuntu:22.04 AS builder
LABEL stage=builder

## Install build tools (C++ compiler, 'g++', 'make')
RUN apt-get update && apt-get install -y --no-install-recommends make build-essential

## Copy whisper.cpp submodule for Stage 1.
COPY deps/whisper.cpp/ /whisper.cpp/
WORKDIR /whisper.cpp

## Compile whisper.cpp
RUN make base

## Download tiny.en model (for testing only)
RUN ./models/download-ggml-model.sh tiny.en

### NOTE: Change to base for increased accuracy and multi-lang support later ###
## RUN ./models/download-ggml-model.sh base


# STAGE 2: Python env
FROM python:3.10-slim

WORKDIR /app

## Copy compiled Whisper.cpp
COPY --from=builder /whisper.cpp/main /usr/local/bin/whisper
COPY --from=builder /whisper.cpp/models/ggml-base.en.bin /app/models/ggml-base.en.bin

## Copy Python application
COPY src/ /app/src/

## Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

## Default executable
ENTRYPOINT ["python", "-m", "src.main"]

# Default fallback
CMD ["--help"]
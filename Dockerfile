# Full Ubuntu env
FROM ubuntu:22.04

## Install build tool dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    build-essential \
    git \
    cmake \
    python3.10 \
    python3-pip \
    && apt-get clean

## Set main application directory
WORKDIR /app
## And add submodule
COPY deps/whisper.cpp/ /app/whisper.cpp/

## Set whisper as working directory
WORKDIR /app/whisper.cpp
## Compile whisper.cpp whisper-cli using cmake
RUN cmake -B build
RUN cmake --build build -j --config Release

# Copy the new executable from its new location to the PATH
RUN cp build/bin/whisper-cli /usr/local/bin/whisper-cli

# Return to the main application directory
WORKDIR /app

# --- Setup Python Application ---
COPY deps/whisper.cpp/models/ggml-base.bin /app/models/ggml-base.bin
COPY src/ /app/src/
COPY requirements.txt .
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

# --- Final Configuration ---
ENTRYPOINT ["python3.10", "-m", "src.main"]
CMD ["--help"]
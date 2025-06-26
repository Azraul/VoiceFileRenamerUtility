# VoiceFileRenamerUtility

A command-line utility that renames audio files based on their transcribed content. *This project serves as a practical demonstration of modern CI/CD and DevOps principles*.

## The Problem

Working with audio files, such as meeting recordings or voice memos, often results in a folder of generically named files like `20250612105213001.wav`. Finding a specific recording requires listening to each one. This tool aims to solve that by renaming files to reflect their actual content, for example: `hello_my_name_is_alf.wav`.

## Features

-   **AI-Powered Transcription:** Use Whisper.cpp engine to accurately transcribe speech to text.
-   **Batch Processing:** Efficiently processes and renames all supported audio files in a directory.
-   **Containerized Environment:** Fully containerized with Docker for a consistent and reproducible environment everywhere.
-   **Automated CI/CD Pipeline:** Every change is automatically tested and validated, preventing broken code from being merged.

## Technology Stack

-   **Application:** Python, Click (for CLI)
-   **AI Model:** Whisper.cpp (running the `ggml-base` multi-language model)
-   **Orchestration:** Docker, Makefile
-   **CI/CD:** GitHub Actions

# DevOps

This project was built with a "DevOps-first" mindset. The focus is on the automation, reliability, and structure of the development lifecycle.

1.  **Multi-Stage Dockerfile:** The `Dockerfile` is optimized using a multi-stage build.
    -   A `builder` stage compiles the C++ dependencies.
    -   A `tester` stage runs the validation suite in a clean environment.
    -   The `final` stage is a lean, production-ready image containing only the necessary application code and binaries.

2.  **Makefile as the "Single Source of Truth":** The `Makefile` acts as the primary interface.
    -   `make`: Defaults to a help for a full command list
    -   `make build`: Creates the final production Docker image.
    -   `make test`: *Currently a simple test from the container*
    -   `make clean`: Cleans up build artifacts.

3.  **Automated Dependency Management:** The CI process runs on a clean machine every time. The `Makefile` automatically detects if the large AI model file is missing and downloads it before starting the build, ensuring the CI pipeline never fails due to a missing dependency.

4.  **Continuous Integration with GitHub Actions:** The workflow in `.github/workflows/ci.yml` is triggered on every pull request to `main`. It uses the `Makefile` to run the test suite, guaranteeing that all checks pass before a merge is allowed.

# Roadmap

-   [X] Setup CI/CD pipeline with container and whisper.cpp
-   [x] Develop core functionality and comprehensive unit and integration tests
-   [ ] Add linter
-   [ ] Publish and release

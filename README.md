# VoiceFileRenamerUtility

[![CI - Build + Validate](https://github.com/Azraul/VoiceFileRenamerUtility/actions/workflows/ci.yml/badge.svg)](https://github.com/Azraul/VoiceFileRenamerUtility/actions/workflows/ci.yml)

A command-line utility that renames audio files based on their transcribed content. This project serves as a practical demonstration of modern CI/CD, DevOps principles, and user-focused tool design and was made to transcribe a few hundred recorded voice lines for a movie project involving robots.

## The Problem

Generically named files like `rec_20250612_1052.wav` are hard to keep track off, finding a specific recording requires listening to each one when editing moves. This tool solves that by renaming files to reflect their actual content, for example: `alf_001_hello_i_am_a_robot.wav`.

## Features

-   **AI-Powered Transcription:** Uses the Whisper.cpp engine to accurately transcribe speech to text.
-   **Multi-Language Support:** Transcribe audio in various languages (e.g., `en`, `sv`, `de`) by specifying a language code.
-   **Batch Processing:** Efficiently processes and renames all supported audio files in a directory.
-   **Containerized Environment:** Fully containerized with Docker for a consistent and reproducible environment that runs anywhere.
-   **Automated CI/CD Pipeline:** Every change is automatically tested and validated, preventing broken code from being merged.

## How to Use This Tool

You only need to have **Docker** installed on your system. The `Makefile` handles everything else.

### Step 1: Prepare Your Folders

1.  Create a folder and place all your audio files (`.wav`, `.mp3`, etc.) inside it.
2.  Create a second, **empty** folder where the renamed files will be saved.

### Step 2: Run the Command

Open your terminal in the project directory and use the `make run` command. You will need to provide the following variables:

*   `INPUT_DIR`: The path to your folder with the raw audio.
*   `OUTPUT_DIR`: The path to your empty output folder.
*   `SPEAKER_ID`: The name or ID you want to use for the speaker.
*   `LANGUAGE`: (Optional) The two-letter language code for transcription. Defaults to `"en"` (English).

#### **Example 1: Processing English Audio**

Let's say your audio is in a folder named `my_raw_recordings` and you want the output in `my_voice_recordings`.

```bash
make run \
  INPUT_DIR="./my_raw_recordings" \
  OUTPUT_DIR="./my_lines" \
  SPEAKER_ID="alf"
```

#### **Example 2: Processing Swedish Audio**

If you have Swedish audio, simply add the `LANGUAGE` variable.

```bash
make run \
  INPUT_DIR="./snow_raw_swedish_recordings" \
  OUTPUT_DIR="./snow_swedish_lines" \
  SPEAKER_ID="snow" \
  LANGUAGE="sv"
```

### Step 3: Check the Output

The tool will run and you will see the transcription process in your terminal. When it's finished, your output folder will be populated with the newly named files.

---

## Technology Stack & Engineering

-   **Application:** Python, Click (for CLI)
-   **AI Model:** Whisper.cpp (running the `ggml-base` multi-language model)
-   **Orchestration:** Docker, Makefile
-   **CI/CD:** GitHub Actions
-   **Testing:** Pytest

### DevOps-First Approach

This project was built to be robust and reliable.

1.  A `Docker` environment for a consistent and reproducible environment that runs anywhere.
2.  The `Makefile` acts as a single, consistent entry point for all common actions, abstracting away complex Docker commands.
3.  The `Makefile` automatically detects if the large AI model file is missing and downloads it before starting the build.
4.  The workflow in `.github/workflows/ci.yml` runs unit tests and a full integration test on every pull request, guaranteeing that all checks pass before a merge is allowed.

### Useful Developer Commands

*   `make build`: Creates the final production Docker image.
*   `make unit-test`: Runs the fast Python unit tests using `pytest`.
*   `make test`: Runs the full end-to-end integration test.
*   `make clean`: Cleans up the built Docker image and test artifacts.
*   `make distclean`: A deep clean that also removes the downloaded AI model.

## Project Roadmap

-   [x] Setup CI/CD pipeline with container and whisper.cpp
-   [x] Develop core functionality and comprehensive unit and integration tests
-   [x] Full run functionality and tesed
-   [x] Multi-language support for increase accuracy.
-   [ ] Add linter (e.g., `flake8` or `black`) to the CI pipeline
-   [ ] Publish and release the image to a container registry

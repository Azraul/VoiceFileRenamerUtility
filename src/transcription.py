import os
import subprocess
import logging

WHISPER_MODEL_PATH = "/app/models/ggml-base.bin"
WHISPER_EXECUTABLE_PATH = "/usr/local/bin/whisper-cli"


def transcribe_audio(file_path: str) -> str | None:
    logging.info(f"Attempting transcription for: {file_path}")
    command = [
        WHISPER_EXECUTABLE_PATH,
        "-f",
        file_path,
        "-m",
        WHISPER_MODEL_PATH,
        "-nt",
    ]
    logging.info(f"Executing command: {' '.join(command)}")
    try:
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, encoding="utf-8"
        )
        transcribed_text = result.stdout.strip()
        if not transcribed_text:
            logging.warning(
                f"Whisper produced no output for {file_path}. The audio might be silent."
            )
            return None
        else:
            logging.info(f"Successfully transcribed: {transcribed_text[:100]}...")
        return transcribed_text
    except FileNotFoundError:
        logging.error(
            f"FATAL: The executable was not found at {WHISPER_EXECUTABLE_PATH}."
        )
        return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Whisper.cpp execution FAILED for {file_path}.")
        logging.error(f"Return Code: {e.returncode}")
        logging.error(f"--- Whisper STDOUT ---\n{e.stdout.strip()}")
        logging.error(f"--- Whisper STDERR ---\n{e.stderr.strip()}")
        return None

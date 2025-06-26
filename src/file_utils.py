import os
import logging
from slugify import slugify

# whisper.cpp supports wav files only
# Feature idea: Add support for more extensions with ffmpeg conversions
SUPPORTED_EXTENSION = ".wav"


def get_audio_files(input_dir: str) -> list[str]:
    """
    Finds, filters, and sorts all supported audio files in a directory.

    Args:
        input_dir: The directory to search.

    Returns:
        A sorted list of full file paths for .wav files.
    """
    logging.info(f"Searching for '{SUPPORTED_EXTENSION}' files in '{input_dir}'...")
    try:
        all_files = os.listdir(input_dir)

        audio_files = [f for f in all_files if f.lower().endswith(SUPPORTED_EXTENSION)]

        if not audio_files:
            logging.warning(f"No '{SUPPORTED_EXTENSION}' files found.")
            return []

        files_with_paths = [os.path.join(input_dir, f) for f in audio_files]
        files_with_paths.sort(key=os.path.getmtime)

        logging.info(f"Found {len(files_with_paths)} audio files to process.")
        return files_with_paths
    except OSError as e:
        logging.error(f"Could not read or sort files in '{input_dir}': {e}")
        return []


def slugify_filename_component(text: str) -> str:
    """
    Sanitizes a string to be a valid filename component with slugify module.
    """
    s = slugify(text, separator="_")
    return s[:80]


def construct_new_filename(
    speaker_id: str,
    recording_number: int,
    transcribed_text: str,
    original_extension: str,
) -> str:
    """Constructs the new filename based on the specified format."""
    sanitized_voiceline = slugify_filename_component(transcribed_text)
    if not sanitized_voiceline:
        sanitized_voiceline = "transcription_failed"
    return f"{speaker_id}_{recording_number}_{sanitized_voiceline}{original_extension}"


def rename_file(old_path: str, new_path: str):
    """Renames a file, handling potential errors."""
    try:
        os.rename(old_path, new_path)
        logging.info(
            f"Successfully renamed '{os.path.basename(old_path)}' to '{os.path.basename(new_path)}'"
        )
    except OSError as e:
        logging.error(f"Error renaming file '{os.path.basename(old_path)}': {e}")

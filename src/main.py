import os
import shutil
import logging
import click
from . import transcription
from . import file_utils

# Setup basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_single_file(
    file_path: str, speaker_id: str, recording_number: int, output_dir: str
):
    """
    Processes a single audio file: copies, transcribes, and renames it.
    """
    filename = os.path.basename(file_path)
    logging.info("-------------------------------------------------")
    logging.info(f"Processing file {recording_number}: {filename}")

    # Copy file to output dir first
    dest_path = os.path.join(output_dir, filename)
    shutil.copy2(file_path, dest_path)

    # Transcribe the copied file
    transcribed_text = transcription.transcribe_audio(dest_path)

    # If transcription returns None (failure), default to an empty string.
    if transcribed_text is None:
        logging.warning(f"Transcription failed for '{filename}'")
        transcribed_text = ""

    # Proceed with renaming unconditionally
    original_ext = os.path.splitext(filename)[1]
    new_filename = file_utils.construct_new_filename(
        speaker_id, recording_number, transcribed_text, original_ext
    )
    new_filepath = os.path.join(output_dir, new_filename)
    file_utils.rename_file(dest_path, new_filepath)


@click.command()
@click.option(
    "--speaker-id", required=True, help='The ID of the speaker (e.g., "alf").'
)
@click.option(
    "--input-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing the raw audio files.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Directory where renamed files will be saved.",
)
def process_audio_files(speaker_id, input_dir, output_dir):
    """
    A command-line tool to batch-rename audio files based on their speech content.
    """
    logging.info("--- Voice Renamer Utility ---")
    logging.info(f"Speaker ID: {speaker_id}")
    logging.info(f"Input Directory: {input_dir}")
    logging.info(f"Output Directory: {output_dir}")

    # Create the output directory, if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Find and get list of sorted files
    audio_files = file_utils.get_audio_files(input_dir)

    if not audio_files:
        logging.warning("No audio files to process.")
        return

    # The main loop, process for each file in audio_file
    for i, file_path in enumerate(audio_files):
        process_single_file(
            file_path=file_path,
            speaker_id=speaker_id,
            recording_number=i + 1,
            output_dir=output_dir,
        )

    logging.info("--- Processing Complete ---")


if __name__ == "__main__":
    process_audio_files()

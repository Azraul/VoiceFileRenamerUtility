import pytest
import os
import time
from src.file_utils import (
    slugify_filename_component,
    construct_new_filename,
    get_audio_files,
)


def test_get_audio_files(tmp_path):
    """
    Tests the get_audio_files function to ensure it finds, filters,
    and sorts files correctly.
    """
    # Arrange: Create a temporary directory structure and dummy files
    audio_dir = tmp_path / "audio_files"
    audio_dir.mkdir()

    # Create files with controlled modification times to test sorting.
    # We create file2 first, so it's older than file1.
    file2_path = audio_dir / "second_file.wav"
    file1_path = audio_dir / "first_file.wav"
    unsupported_file = audio_dir / "document.txt"

    file2_path.touch()
    time.sleep(0.1)  # A small delay to guarantee different timestamps
    file1_path.touch()
    unsupported_file.touch()

    # Act: Call the function we want to test
    result = get_audio_files(str(audio_dir))

    # Assert: Check that the results are correct
    assert len(result) == 2, "Should only find the two supported audio files"

    # Check that the files are sorted by modification time (oldest first)
    assert os.path.basename(result[0]) == "second_file.wav"
    assert os.path.basename(result[1]) == "first_file.wav"


def test_sanitize_filename_component():
    assert slugify_filename_component("HeLlO, tHeRe?!") == "hello_there"
    assert slugify_filename_component("What are you doing?") == "what_are_you_doing"
    assert (
        slugify_filename_component("  leading and trailing spaces  ")
        == "leading_and_trailing_spaces"
    )
    long_string = "a" * 100
    assert len(slugify_filename_component(long_string)) == 80


def test_construct_new_filename():
    expected = "alf_1_i_am_a_robot.wav"
    actual = construct_new_filename(
        speaker_id="alf",
        recording_number=1,
        transcribed_text="I am a robot!",
        original_extension=".wav",
    )
    assert actual == expected


def test_construct_filename_with_empty_transcription():
    expected = "alf_5_transcription_failed.wav"
    actual = construct_new_filename(
        speaker_id="alf",
        recording_number=5,
        transcribed_text="",
        original_extension=".wav",
    )
    assert actual == expected

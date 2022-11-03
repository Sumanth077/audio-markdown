"""Test audio-to-markdown package via integration tests."""
import base64
import mimetypes
import time

import pytest
from steamship import PackageInstance, Steamship
from steamship.base import TaskState

from tests import TEST_DATA

HANDLE = "audio-markdown-staging"


def _get_instance():
    client = Steamship(workspace="audio-markdown-staging-test-003")
    instance = PackageInstance.create(client, package_handle=HANDLE, config={})
    assert instance is not None
    assert instance.id is not None
    return instance


def test_package() -> None:
    """Test the entire package, using the 'transcribe' endpoint (to avoid audio upload)."""
    instance = _get_instance()

    audio_input = TEST_DATA / "input.m4a"
    mime_type, _ = mimetypes.guess_type(audio_input)
    with audio_input.open("rb") as audio:
        encoded = base64.b64encode(audio.read()).decode("ISO-8859-1")
        transcribe = instance.invoke("transcribe", encoded_audio=encoded, mime_type=mime_type)

    task_id = transcribe["task_id"]
    status = transcribe["status"]

    retries = 0
    while retries <= 100 and status != TaskState.succeeded:
        response = instance.invoke("get_markdown", task_id=task_id)
        status = response["status"]
        if status == TaskState.failed:
            break

        print(f"[Try {retries}] Transcription {status}.")
        if status == TaskState.succeeded:
            break
        time.sleep(2)
        retries += 1

    if status == TaskState.failed:
        pytest.fail(f"task failed: {response}")

    got = response["markdown"]

    want_path = TEST_DATA / "output.md"
    want = open(want_path).read()
    assert got == want

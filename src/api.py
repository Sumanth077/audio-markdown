"""Package that generates Markdown transcriptions of audio with inline formatting."""
import base64
import json
from pathlib import Path
from typing import Optional

import requests
import toml
from pydantic import HttpUrl
from steamship import File, MimeTypes
from steamship.base import Task, TaskState
from steamship.invocable import InvocableResponse, PackageService, create_handler, post

from transcript_to_markdown import transcript_to_markdown


class AudioMarkdownPackage(PackageService):
    """Package that transcribes audio to Markdown using in-audio formatting cues."""

    BLOCKIFIER_HANDLE = "whisper-s2t-blockifier"
    BLOCKIFIER_INSTANCE_HANDLE = "whisper-s2t-blockifier-instance-001"

    def __init__(self, **kwargs):
        secret_kwargs = toml.load(str(Path(__file__).parent / ".steamship" / "secrets.toml"))
        kwargs["config"] = {
            **secret_kwargs,
            **{k: v for k, v in kwargs["config"].items() if v != ""},
        }
        super().__init__(**kwargs)

        # todo(douglas-reid): does hard-coding the instance handle make this brittle per-workspace?
        self.s2t_blockifier = self.client.use_plugin(
            plugin_handle=self.BLOCKIFIER_HANDLE,
            instance_handle=self.BLOCKIFIER_INSTANCE_HANDLE,
            config={"whisper_model": "base", "get_segments": False},
            fetch_if_exists=True,
        )

    @post("transcribe_url")
    def transcribe_url(
        self, url: HttpUrl, mime_type: Optional[MimeTypes] = None
    ) -> InvocableResponse:
        """Transcribe audio from URL."""
        file = File.create(
            self.client, content=requests.get(url).content, mime_type=(mime_type or MimeTypes.MP3)
        )
        return self._transcribe_audio_file(file)

    @post("transcribe")
    def transcribe(self, encoded_audio: str, mime_type: str = MimeTypes.MP3) -> InvocableResponse:
        """Summarize audio using AssemblyAI."""
        raw_audio = base64.b64decode(encoded_audio)
        file = File.create(self.client, content=raw_audio, mime_type=(mime_type or MimeTypes.MP3))
        return self._transcribe_audio_file(file)

    @post("get_markdown")
    def get_markdown(self, task_id: str):
        """Get the markdown for a transcribed audio file based on task_id."""
        task = Task.get(self.client, _id=task_id)
        if task.state != TaskState.succeeded:
            return InvocableResponse(
                json={
                    "task_id": task.task_id,
                    "status": task.state,
                    "status_message": task.status_message,
                }
            )

        file_id = json.loads(task.input)["id"]
        file = File.get(self.client, file_id)
        transcript_text = file.blocks[0].text
        markdown_text = transcript_to_markdown(transcript_text)
        return InvocableResponse(
            json={
                "markdown": markdown_text,
                "status": task.state,
                "status_message": task.status_message,
            }
        )

    def _transcribe_audio_file(self, file) -> InvocableResponse:
        task = file.blockify(plugin_instance=self.s2t_blockifier.handle)
        return InvocableResponse(
            json={
                "task_id": task.task_id,
                "status": task.state,
                "status_message": task.status_message,
            }
        )


handler = create_handler(AudioMarkdownPackage)

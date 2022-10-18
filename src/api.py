"""Package that generates Markdown transcriptions of audio with inline formatting."""
import base64
import pathlib
from typing import Optional, Type

import requests
import toml
from pydantic import HttpUrl
from steamship import File, MimeTypes, PluginInstance
from steamship.app import App, Response, create_handler, post
from steamship.plugin.config import Config

PRIORITY_LABEL = "priority"


class AudioMarkdownPackage(App):
    """Package that transcribes audio to Markdown using in-audio formatting cues."""

    BLOCKIFIER_HANDLE = "s2t-blockifier-default"

    class AudioMarkdownPackageConfig(Config):
        """Config object containing required configuration parameters to initialize a AudioMarkdownPackage."""

        pass

    def config_cls(self) -> Type[Config]:
        """Return the Configuration class."""
        return self.AudioMarkdownPackageConfig

    def __init__(self, **kwargs):
        secret_kwargs = toml.load(
            str(pathlib.Path(__file__).parent / ".steamship" / "secrets.toml")
        )
        kwargs["config"] = {
            **secret_kwargs,
            **{k: v for k, v in kwargs["config"].items() if v != ""},
        }
        super().__init__(**kwargs)

        self.s2t_blockifier = PluginInstance.create(
            self.client,
            plugin_handle=self.BLOCKIFIER_HANDLE,
            config={},
        ).data

    @post("transcribe_url")
    def transcribe_url(self, url: HttpUrl, mime_type: Optional[MimeTypes] = None) -> Response:
        """Transcribe audio from URL."""
        mime_type = mime_type or MimeTypes.MP3
        file = File.create(self.client, content=requests.get(url).content, mime_type=mime_type).data
        return self._transcribe_audio_file(file)

    @post("transcribe")
    def transcribe(self, audio: str, mime_type: str = MimeTypes.MP3) -> Response:
        """Summarize audio using AssemblyAI."""
        audio = base64.b64decode(audio.encode("utf-8"))
        file = File.create(self.client, content=audio, mime_type=mime_type).data
        return self._transcribe_audio_file(file)

    @post("get_markdown")
    def get_markdown(self, task_id: str):
        """Get the markdown for a transcribed audio file based on task_id."""
        # task = Task.get(self.client, _id=task_id).data
        # if task.state != TaskState.succeeded:
        #     return InvocableResponse(json={"task_id": task.task_id, "status": task.state})
        # else:
        #     file_id = json.loads(task.input)["id"]
        #     file = File.get(self.client, file_id).data
        #     return InvocableResponse(json={"task_id": task.task_id, "status": task.state, "file": file.dict()})

    def _transcribe_audio_file(self, file) -> Response:
        status = file.blockify(plugin_instance=self.s2t_blockifier.handle)
        task = status.task
        return Response(json={"task_id": task.task_id, "status": task.state})


handler = create_handler(AudioMarkdownPackage)

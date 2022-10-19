# Steamship Audio Markdown Package 

This project contains a Steamship Package that transcribes audio, generating Markdown output. The generated
Markdown will be formatted based on cues within the transcribed audio itself.

Web demo: https://audio-to-markdown.steamship.com/

## Usage

```python
import time

from steamship import Steamship
from steamship.base import TaskState


instance = Steamship.use("audio-markdown", "my-workspace-name")

url = "<url to mp3 file>"
transcribe_task = instance.post("transcribe_url", url=url).data
task_id = transcribe_task["task_id"]
status = transcribe_task["status"]

# Wait for completion
n_retries = 0
while n_retries <= 100 and status != TaskState.succeeded:
    response = instance.post("get_markdown", task_id=task_id)

    if response.task and response.task.state == TaskState.failed:
        print(f"[FAILED] {response.task.status_message}")
        break

    status = response.data["status"]

    print(f"[Try {n_retries}] Transcription is {status}.")
    if status == "succeeded":
        break
    time.sleep(2)
    n_retries += 1

# Get Markdown
response = instance.post("get_markdown", task_id=task_id)
markdown = response.data["markdown"]
```

## Developing

Development instructions are located in [DEVELOPING.md](DEVELOPING.md)

## Deploying

Deployment instructions are located in [DEPLOYING.md](DEPLOYING.md)

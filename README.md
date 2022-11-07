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
transcribe_task = instance.invoke("transcribe_url", url=url)
task_id = transcribe_task["task_id"]
status = transcribe_task["status"]

# Wait for completion
retries = 0
while retries <= 100 and status != TaskState.succeeded:
    response = instance.invoke("get_markdown", task_id=task_id)
    status = response["status"]
    if status == TaskState.failed:
        print(f"[FAILED] {response['status_message']")
        break

    print(f"[Try {retries}] Transcription {status}.")
    if status == TaskState.succeeded:
        break
    time.sleep(2)
    retries += 1

# Get Markdown
markdown = response["markdown"]
```

## Developing

Development instructions are located in [DEVELOPING.md](DEVELOPING.md)

## Deploying

Deployment instructions are located in [DEPLOYING.md](DEPLOYING.md)

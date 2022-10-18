# Steamship Audio Markdown Package 

This project contains a Steamship Package that transcribes audio, generating Markdown output. The generated
Markdown will be formatted based on cues within the transcribed audio itself.

## Usage

```python
from steamship import Steamship, Tag

instance = Steamship.use("audio-markdown", "my-workspace-name")

url = "<url to mp3 file>"
transcribe_task = instance.post("transcribe_url", url=url).data

# Wait for completion
...

# Get Markdown
```

## Developing

Development instructions are located in [DEVELOPING.md](DEVELOPING.md)

## Testing

Testing instructions are located in [TESTING.md](TESTING.md)

## Deploying

Deployment instructions are located in [DEPLOYING.md](DEPLOYING.md)

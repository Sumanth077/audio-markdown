# Developing

You can easily fork, customize, and republish this plugin with new functionality.

## Change the Handle

Plugin handles are unique in Steamship. Think of them like you think of an NPM or Pip package name.

To customize and re-deploy this repository as your own, first edit the `handle` propery of `steamship.json` to create a new handle name.

## Set up your Virtual Environment

We recommend using Python virtual environments for development.
To set one up, run the following command from this directory:

```bash
python3 -m venv .venv
```

Activate your virtual environment by running:

```bash
source .venv/bin/activate
```

Your first time, install the required dependencies with:

```bash
python -m pip install -r requirements.dev.txt
python -m pip install -r requirements.txt
```

## Develop

All the code for this package is located in the `src/api.py` file.

This project is a package that transcribes audio and formats the transcription according to formatting cues within the transcription.

## Throw, Log, and Test!

Your package code will be executing (1) remotely, (2) automatically, and (3) potentially at high-scale. This makes it critical that you:

* Throw detailed exceptions eagerly
* Log liberally
* Write unit tests

See `TESTING.md` for details on the pre-configured testing setup.

## Deploying

To run this plugin on Steamship, you must first deploy it. 

See `DEPLOYING.md` for instructions.
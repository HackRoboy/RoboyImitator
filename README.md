# RoboyImitator

## Description

In this project we record emotions and voice from your personal computer and project
those onto Roboy.

For speech-to-text, text-to-speech and emotion detection Microsoft Azure Cognitive Services are used.
For speech-to-text `speech_to_text/recognition_node.py` creates a ros2 service at
`/roboy/cognition/speech/recognition`.

## Running RoboyImitator

This project consists of two parts:

1. Servers on your personal computer for emotion detection and microphone recording
2. Recognition node and main loop which connects to your servers and performs `pyroboy.listen()`,
`pyroboy.say("bla")`, `pyroboy.show_emotion()`.

### Local installation

1. Run `pip install -r requirements && pip install -e .` to install the necessary python packages.
2. Create a file called `secrets.yaml` inside of the configs folder with the following keys and their
corresponding values: `stt_key, tts_key, face_key, service_region` where the keys are from Microsoft Cognitive
Services.

### Roboy installation

```
docker-compose up --detach imitator
```

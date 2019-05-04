from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
import time
import wave
import yaml
import sys


CONFIGS_PATH = Path("../../configs/secrets.yaml")

with open(CONFIGS_PATH) as stream:
    CONFIGS = yaml.load(stream)

speech_key, service_region = CONFIGS["stt_key"], CONFIGS["service_region"]


def speech_recognition_with_push_stream():
    """gives an example how to use a push audio stream to recognize speech from a custom audio
    source"""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    import pyaudio
    FORMAT = pyaudio.paInt16  # We use 16 bit format per sample
    CHANNELS = 1
    RATE = 16000
    CHUNK = 3200  # 1024 bytes of data read from the buffer
    RECORD_SECONDS = 0.1

    audio = pyaudio.PyAudio()


    # setup the audio stream
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    # instantiate the speech recognizer with push stream input
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Connect callbacks to the events fired by the speech recognizer
    #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    # The number of bytes to push per buffer
    # n_bytes = 3200
    # wav_fh = wave.open(weatherfilename)

    # start continuous speech recognition
    speech_recognizer.start_continuous_recognition()

    # Claim the microphone
    mic_stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True)

    # start pushing data until all data has been read from the file
    try:
        while(True):
            #frames = wav_fh.readframes(n_bytes // 2)
            frames = mic_stream.read(CHUNK)
            if not frames:
                break

            stream.write(frames)
    finally:
        mic_stream.stop_stream()
        speech_recognizer.stop_continuous_recognition()
        stream.close()
        mic_stream.close()


if __name__ == "__main__":
    speech_recognition_with_push_stream()

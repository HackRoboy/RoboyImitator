from roboy_imitator.common import CONFIGS
from roboy_imitator.speech_to_text.mic_client import MicrophoneClient

import azure.cognitiveservices.speech as speechsdk
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 3200


class SpeechToText:

    def __init__(self, key=CONFIGS["stt_key"], region=CONFIGS["service_region"]):
        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)

    def recognize(self, mic_source=None):
        # setup the audio stream
        stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        local_mic = True if mic_source is None else False

        if mic_source is None:
            audio = pyaudio.PyAudio()
            # Claim the microphone
            mic_source = audio.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True)

        # instantiate the speech recognizer with push stream input
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        recognized = False
        recognized_text = ''

        # Connect callbacks to the events fired by the speech recognizer
        #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        def recognized_handler(evt):
            nonlocal recognized
            nonlocal recognized_text
            print('RECOGNIZED: {}'.format(evt.result.text))
            recognized = True
            recognized_text = evt.result.text

        speech_recognizer.recognized.connect(recognized_handler)
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

        speech_recognizer.start_continuous_recognition()

        try:
            with mic_source:
                while not recognized:
                    frames = mic_source.read(CHUNK)
                    if not frames:
                        break
                    stream.write(frames)
                return recognized_text
        except KeyboardInterrupt:
            pass
        finally:
            if local_mic:
                mic_source.stop_stream()
            speech_recognizer.stop_continuous_recognition()
            stream.close()


if __name__ == "__main__":
    speech_to_text = SpeechToText(CONFIGS["stt_key"], CONFIGS["service_region"])
    mic_client = MicrophoneClient(host="192.168.64.1", port=10002, chunk_size=4096)
    speech_to_text.recognize(mic_client.stream)

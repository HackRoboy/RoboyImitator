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

        # setup the audio stream
        self.stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=self.stream)

        self._reset()

        # instantiate the speech recognizer with push stream input
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        # Connect callbacks to the events fired by the speech recognizer
        #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        def recognized_handler(evt):
            print('RECOGNIZED: {}'.format(evt.result.text))
            self.recognized = True
            self.recognized_text = evt.result.text

        self.speech_recognizer.recognized.connect(recognized_handler)
        self.speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        self.speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        self.speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        self.speech_recognizer.start_continuous_recognition()

    def recognize(self, mic_source):
        self._reset()
        try:
            with mic_source:
                while not self.recognized:
                    frames = mic_source.stream.read(CHUNK)
                    if not frames:
                        break
                    self.stream.write(frames)
                return self.recognized_text
        except KeyboardInterrupt:
            pass

    def _reset(self):
        self.recognized = False
        self.recognized_text = ''

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.speech_recognizer.stop_continuous_recognition()
        self.stream.close()



if __name__ == "__main__":
    speech_to_text = SpeechToText(CONFIGS["stt_key"], CONFIGS["service_region"])
    mic_client = MicrophoneClient(host="192.168.64.1", port=10002, chunk_size=4096)
    speech_to_text.recognize(mic_client.stream)

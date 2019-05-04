from roboy_imitator.face import mimic_emotions
from threading import Thread
import pyroboy
import logging


def main():
    try:
        emotion_thread = Thread(target=mimic_emotions)
        emotion_thread.setDaemon(True)
        emotion_thread.start()

        while True:
            phrase = pyroboy.listen()
            pyroboy.say(phrase)
    except:
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

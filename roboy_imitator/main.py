from roboy_imitator.communication.emotions import receive_emotions
from threading import Thread
from multiprocessing import Process
from roboy_imitator.speech_to_text.recognition_node import client_recognition
import pyroboy
import logging
import click


@click.command()
@click.option('--emotion_host', default="localhost", help='Emotion host which sends emotion indices')
@click.option('--emotion_port', default=10000, help='Emotion port', type=int)
@click.option('--mic_host', default="localhost", help='Microphone host which sends recording chunks')
@click.option('--mic_port', default=10001, help='Microphone port', type=int)
def main(emotion_host, emotion_port, mic_host, mic_port):
    try:
        # Start the transcription service
        process = Process(target=client_recognition, args=(mic_host, mic_port))
        process.start()

        # Start the emotion receiving server
        emotion_thread = Thread(target=emotion_loop, args=(emotion_host, emotion_port))
        emotion_thread.setDaemon(True)
        emotion_thread.start()

        while True:
            phrase = pyroboy.listen()
            pyroboy.say(phrase)
    except:
        pass


def emotion_loop(host, port):
    for emotion in receive_emotions(host, port):
        pyroboy.show_emotion(emotion)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

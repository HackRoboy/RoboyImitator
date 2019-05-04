from roboy_imitator.communication.emotions import receive_emotions
from threading import Thread
from multiprocessing import Process
from roboy_imitator.speech_to_text.recognition_node import client_recognition_service
import pyroboy
import logging
import click
import time
import rclpy

@click.command()
@click.option('--emotion_host', default="localhost", help='Emotion host which sends emotion indices')
@click.option('--emotion_port', default=10000, help='Emotion port', type=int)
@click.option('--mic_host', default="localhost", help='Microphone host which sends recording chunks')
@click.option('--mic_port', default=10001, help='Microphone port', type=int)
def main(emotion_host, emotion_port, mic_host, mic_port):
    try:
        # Start the transcription service
        #stt_thread = Process(target=client_recognition_service, args=(pyroboy.node, mic_host, mic_port))
        #stt_thread.start()
        #time.sleep(4)
        # Start the emotion receiving server
        emotion_thread = Thread(target=emotion_loop, args=(emotion_host, emotion_port))
        emotion_thread.setDaemon(True)
        emotion_thread.start()

        while True:
            #rclpy.spin_once(pyroboy.node)
            #time.sleep(0.5)
            print("listening again..")
            phrase = pyroboy.listen()
            if len(phrase) == 0:
                continue
            pyroboy.say(phrase)
    except:
        pass


def emotion_loop(host, port):
    for emotion in receive_emotions(host, port):
        print(emotion)
        pyroboy.show_emotion(emotion)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

from roboy_imitator.communication.emotions import receive_emotions
from threading import Thread
import pyroboy
import logging
import click


@click.command()
@click.option('--emotion_host', default="192.168.0.215", help='Emotion host which sends emotion indices')
@click.option('--emotion_port', default=10001, help='Emotion port', type=int)
def main(emotion_host, emotion_port):
    try:
        # Start the emotion receiving client
        emotion_thread = Thread(target=emotion_loop, args=(emotion_host, emotion_port))
        emotion_thread.setDaemon(True)
        emotion_thread.start()

        while True:
            logging.info("Listening again..")
            phrase = pyroboy.listen()
            if len(phrase) == 0:
                continue
            logging.info(f"You said {phrase}")
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
